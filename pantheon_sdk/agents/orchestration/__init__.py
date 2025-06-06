from pantheon_sdk.agents.const import EntrypointGroup
from pantheon_sdk.agents.utils import get_entrypoint


def workflow_builder():
    config = get_entrypoint(EntrypointGroup.AGENT_WORKFLOW_CONFIG_ENTRYPOINT).load()

    return get_entrypoint(EntrypointGroup.AGENT_WORKFLOW_ENTRYPOINT).load()(config())
