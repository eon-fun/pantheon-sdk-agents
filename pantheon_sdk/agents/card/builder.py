from typing import Annotated

from pydantic import Field

from pantheon_sdk.agents.abc import (
    AbstractAgentCard,
    AbstractAgentInputModel,
    AbstractAgentOutputModel,
    AbstractAgentParamsModel,
    BaseAgentInputModel,
    BaseAgentOutputModel,
)
from pantheon_sdk.agents.card.config import get_card_config
from pantheon_sdk.agents.card.models import AgentCard, AgentSKill


class GoalHandleParamsModel(AbstractAgentParamsModel):
    goal: Annotated[str, Field(description="The goal to handle")]


class GoalHandleInputModel(AbstractAgentInputModel):
    context: Annotated[BaseAgentInputModel, Field(description="The context of the request")]


class GoalHandleOutputModel(AbstractAgentOutputModel):
    result: Annotated[BaseAgentOutputModel, Field(description="The result of the request")]


def add_handle_goal_skill() -> AgentSKill:
    return AgentSKill(
        id="handle-goal",
        name="Handle all requests",
        description="This skill handles all requests",
        path="/{goal}",
        params_schema=GoalHandleParamsModel,
        input_schema=GoalHandleInputModel,
        output_schema=GoalHandleOutputModel,
    )


def get_agent_card() -> AbstractAgentCard:
    config = get_card_config()
    return AgentCard(
        name=config.name,
        version=config.version,
        description=config.description,
        skills=[
            add_handle_goal_skill(),
        ],
    )
