from jinja2 import Environment
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

from pantheon_sdk.agents.abc import AbstractPromptBuilder
from pantheon_sdk.agents.prompt.config import BasicPromptConfig
from pantheon_sdk.agents.prompt.const import FINISH_ACTION, HANDOFF_ACTION
from pantheon_sdk.agents.prompt.utils import get_environment


class PromptBuilder(AbstractPromptBuilder):
    def __init__(self, config: BasicPromptConfig, jinja2_env: Environment):
        self.config = config
        self.jinja2_env = jinja2_env

    def generate_plan_prompt(self, *args, system_prompt: str, **kwargs) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    self.jinja2_env.get_template(self.config.system_prompt_template).render(system_prompt=system_prompt)
                ),
                HumanMessagePromptTemplate.from_template(
                    self.jinja2_env.get_template(self.config.chat_template).render(
                        finish_action=FINISH_ACTION,
                        handoff_action=HANDOFF_ACTION,
                        examples=self.jinja2_env.get_template(self.config.generate_plan_examples_template).render(
                            finish_action=FINISH_ACTION,
                            handoff_action=HANDOFF_ACTION,
                        ),
                    )
                ),
            ]
        )

    def generate_chat_prompt(
        self, *args, system_prompt: str, user_prompt: str, context: str, **kwargs
    ) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    self.jinja2_env.get_template(self.config.system_prompt_template).render(system_prompt=system_prompt)
                ),
                HumanMessagePromptTemplate.from_template(
                    self.jinja2_env.get_template(self.config.chat_template).render(
                        context=context,
                        user_message=user_prompt,
                    )
                ),
            ]
        )

    def generate_intent_classifier_prompt(
        self, *args, system_prompt: str, user_prompt: str, **kwargs
    ) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    self.jinja2_env.get_template(self.config.system_prompt_template).render(system_prompt=system_prompt)
                ),
                HumanMessagePromptTemplate.from_template(
                    self.jinja2_env.get_template(self.config.intent_classifier_template).render(
                        user_message=user_prompt,
                        examples=self.jinja2_env.get_template(self.config.intent_classifier_examples_template),
                    )
                ),
            ]
        )

    def generate_reconfigure_prompt(
        self, *args, system_prompt: str, user_prompt: str, existing_config: str, **kwargs
    ) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    self.jinja2_env.get_template(self.config.system_prompt_template).render(system_prompt=system_prompt)
                ),
                HumanMessagePromptTemplate.from_template(
                    self.jinja2_env.get_template(self.config.update_config_template).render(
                        user_message=user_prompt,
                        existing_config=existing_config,
                        examples=self.jinja2_env.get_template(self.config.update_config_examples_template),
                    )
                ),
            ]
        )


def prompt_builder(config: BasicPromptConfig) -> PromptBuilder:
    return PromptBuilder(config, get_environment(config.template_path))
