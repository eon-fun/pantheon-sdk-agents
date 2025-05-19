from collections.abc import Sequence
from logging import getLogger
from typing import Any
from urllib.parse import urljoin

import requests
from ray.serve.deployment import Application

from base_agent import abc
from base_agent.ai_registry import ai_registry_builder
from base_agent.bootstrap import bootstrap_main
from base_agent.card.models import AgentCard
from base_agent.config import BasicAgentConfig, get_agent_config
from base_agent.domain_knowledge import light_rag_builder
from base_agent.langchain import executor_builder
from base_agent.memory import memory_builder
from base_agent.models import (
    AgentModel,
    GoalModel,
    HandoffParamsModel,
    InsightModel,
    MemoryModel,
    QueryData,
    ToolModel,
    Workflow,
)
from base_agent.prompt import prompt_builder

logger = getLogger(__name__)


class BaseAgent(abc.AbstractAgent):
    """Base default implementation for all agents."""

    workflow_runner: abc.AbstractWorkflowRunner
    prompt_builder: abc.AbstractPromptBuilder
    agent_executor: abc.AbstractExecutor

    def __init__(self, config: BasicAgentConfig, *args, **kwargs):
        self.config = config
        self.agent_executor = executor_builder()
        self.prompt_builder = prompt_builder()

        # ---------- AI Registry ----------#
        self.ai_registry_client = ai_registry_builder()

        # ---------- LightRAG Memory -------#
        self.lightrag_client = light_rag_builder()

        # ---------- Redis Memory ----------#
        self.memory_client = memory_builder()

    async def handle(
        self,
        goal: str,
        plan: dict | None = None,
        context: abc.BaseAgentInputModel | None = None,
    ) -> abc.BaseAgentOutputModel:
        """This is one of the most important endpoints of MAS.
        It handles all requests made by handoff from other agents or by user.

        If a predefined plan is provided, it skips plan generation and executes the plan directly.
        Otherwise, it follows the standard logic to generate a plan and execute it.
        """

        if plan is not None and plan:
            result = self.run_workflow(plan, context)
            self.store_interaction(goal, plan, result, context)
            return result

        insights = self.get_relevant_insights(goal)
        past_interactions = self.get_past_interactions(goal)
        agents = self.get_most_relevant_agents(goal)
        tools = self.get_most_relevant_tools(goal, agents)

        plan = self.generate_plan(
            goal=goal,
            agents=agents,
            tools=tools,
            insights=insights,
            past_interactions=past_interactions,
            plan=None,
        )

        result = self.run_workflow(plan, context)
        self.store_interaction(goal, plan, result, context)
        # return result

    def get_past_interactions(self, goal: str) -> list[dict]:
        return self.memory_client.read(key=goal)
        # return [{}]

    def store_interaction(
        self,
        goal: str,
        plan: dict,
        result: abc.BaseAgentOutputModel,
        context: abc.BaseAgentInputModel | None = None,
    ) -> None:
        interaction = MemoryModel(
            **{
                "goal": goal,
                "plan": plan,
                "result": result.model_dump(),
                "context": context.model_dump(),
            }
        )
        self.memory_client.store(key=goal, interaction=interaction.model_dump())

    def get_relevant_insights(self, goal: str) -> list[InsightModel]:
        """Retrieve relevant insights from LightRAG memory for the given goal."""
        response = self.lightrag_client.query(query=goal)
        return [InsightModel(**response)]
        # return []

    def get_most_relevant_agents(self, goal: str) -> list[AgentModel]:
        """This method is used to find the most useful agents for the given goal."""
        response = self.ai_registry_client.post(
            endpoint=self.ai_registry_client.endpoints.find_agents,
            json=QueryData(goal=goal).model_dump(),
        )

        if not response:
            return []

        return [AgentModel(**agent) for agent in response]
        # return [AgentModel(
        #     name = 'example-agent',
        #     description = 'This is an agent to handoff the any goal',
        #     version = '0.1.0'
        # )]

    def get_most_relevant_tools(self, goal: str, agents: list[AgentModel]) -> list[ToolModel]:
        """
        This method is used to find the most useful tools for the given goal.

        """
        response = self.ai_registry_client.post(
            endpoint=self.ai_registry_client.endpoints.find_tools,
            json=GoalModel(goal=goal).model_dump(),
        )
        tools = [ToolModel(**tool) for tool in response]

        for agent in agents:
            card_url = urljoin(agent.endpoint, "/card")
            try:
                resp = requests.get(card_url)
                resp.raise_for_status()

                data = resp.json()
                card = AgentCard(**data)
            except Exception as e:
                logger.warning(f"Failed to fetch card from agent {agent} at {card_url}: {e}")
                continue
            for skill in card.skills:
                func_name = f"{agent.name}_{skill.id}".replace("-", "_")
                spec = {
                    "type": "function",
                    "function": {
                        "name": func_name,
                        "description": skill.description,
                        "parameters": skill.input_model.model_json_schema(),
                        "output": skill.output_model.model_json_schema(),
                    },
                }
                tools.append(
                    ToolModel(
                        name="handoff-tool",
                        version="0.1.0",
                        default_parameters=HandoffParamsModel(
                            endpoint=agent.endpoint, path=skill.path, method=skill.method
                        ).model_dump(),
                        parameters_spec=skill.params_model.model_json_schema(),
                        openai_function_spec=spec,
                    )
                )

        return tools + [
            ToolModel(
                name="return-answer-tool",
                version="0.1.2",
                openai_function_spec={
                    "type": "function",
                    "function": {
                        "name": "return_answer_tool",
                        "description": "Returns the input as output.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "answer": {
                                    "type": "string",
                                    "description": "The answer in JSON string.",
                                    "default": '{"result": 42}',
                                }
                            },
                            "required": ["answer"],
                        },
                        "output": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "string",
                                    "description": "Returns the input as output in JSON string.",
                                }
                            },
                        },
                    },
                },
            ),
        ]

    def generate_plan(
        self,
        goal: str,
        agents: Sequence[AgentModel],
        tools: Sequence[ToolModel],
        past_interactions: Sequence[MemoryModel],
        insights: Sequence[InsightModel],
        plan: dict | None = None,
    ):
        """This method is used to generate a plan for the given goal."""
        return self.agent_executor.generate_plan(
            self.prompt_builder.generate_plan_prompt(system_prompt=self.config.system_prompt),
            available_functions=tools,
            available_agents=agents,
            goal=goal,
            past_interactions=past_interactions,
            insights=insights,
            plan=plan,
        )

    def run_workflow(
        self,
        plan: Workflow,
        context: abc.BaseAgentInputModel | None = None,
    ) -> abc.BaseAgentOutputModel:
        return self.workflow_runner.run(plan, context)

    def reconfigure(self, config: dict[str, Any]):
        self.workflow_runner.reconfigure(config)

    async def handoff(self, endpoint: str, goal: str, plan: dict):
        """This method means that agent can't find a solution (wrong route/wrong plan/etc)
        and decide to handoff the task to another agent."""
        return requests.post(urljoin(endpoint, goal), json=plan).json()


def agent_builder(args: dict) -> Application:
    return bootstrap_main(BaseAgent).bind(config=get_agent_config(**args))
