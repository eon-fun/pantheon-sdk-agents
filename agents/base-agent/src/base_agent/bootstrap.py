from contextlib import asynccontextmanager

from fastapi import FastAPI

from base_agent import abc
from base_agent.orchestration import workflow_builder
from base_agent.card import card_builder



def bootstrap_main(agent_cls: type[abc.AbstractAgent]) -> type[abc.AbstractAgent]:
    """Bootstrap a main agent with the necessary components to be able to run as a Ray Serve deployment."""
    from ray import serve

    runner: abc.AbstractWorkflowRunner = workflow_builder()
    card: abc.AbstractAgentCard = card_builder()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # launch some tasks on app start
        yield
        # handle clean up

    app = FastAPI(lifespan=lifespan)

    @serve.deployment
    @serve.ingress(app)
    class Agent(agent_cls):
        @property
        def workflow_runner(self):
            return runner

        @property
        def agent_card(self):
            return card

        @fastapi.post("/card")
        async def get_card(self):
            return self.agent_card

        @fastapi.get("/workflows")
        async def list_workflows(self, status: str | None = None):
            return await self.workflow_runner.list_workflows(status)

        @fastapi.post("/{goal}")
        async def handle(self, goal: str, plan: dict | None = None, context: Any = None):
            return await super().handle(goal, plan, context)

    return Agent
