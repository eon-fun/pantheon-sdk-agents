from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from pantheon_sdk.agents.abc import AbstractChatResponse, AbstractExecutor
from pantheon_sdk.agents.langchain.config import BasicLangChainConfig, LangChainConfigWithLangfuse
from pantheon_sdk.agents.prompt.parser import AgentOutputPlanParser


class ChatResponse(AbstractChatResponse):
    session_uuid: str


class LangChainExecutor(AbstractExecutor):
    def __init__(self, config: BasicLangChainConfig | LangChainConfigWithLangfuse):
        self.config = config

        self._callbacks = []
        if self.config.langfuse_enabled:
            self._init_langfuse_callback()

    def _init_langfuse_callback(self):
        from langfuse.callback import CallbackHandler

        self._callbacks.append(
            CallbackHandler(
                public_key=self.config.langfuse_public_key.get_secret_value(),
                secret_key=self.config.langfuse_secret_key.get_secret_value(),
                host=self.config.langfuse_host,
            )
        )

    def generate_plan(self, prompt: PromptTemplate, **kwargs) -> str:
        agent = ChatOpenAI(callbacks=self._callbacks, model=self.config.openai_api_model)
        output_parser = StrOutputParser()
        if "available_functions" in kwargs:
            agent.bind_tools(tools=[tool.openai_function_spec for tool in kwargs["available_functions"]])
            output_parser = AgentOutputPlanParser(tools=kwargs["available_functions"])

        kwargs["available_functions"] = "\n".join(
            [tool.render_function_spec() for tool in kwargs["available_functions"]]
        )

        chain = prompt | agent | output_parser

        return chain.invoke(input=kwargs)

    def chat(self, prompt: PromptTemplate, **kwargs) -> str:
        agent = ChatOpenAI(callbacks=self._callbacks, model=self.config.openai_api_model)
        output_parser = StrOutputParser()
        chain = prompt | agent | output_parser
        return chain.invoke(input=kwargs)

    def classify_intent(self, prompt: PromptTemplate, **kwargs) -> str:
        agent = ChatOpenAI(callbacks=self._callbacks, model=self.config.openai_api_model)
        output_parser = StrOutputParser()
        chain = prompt | agent | output_parser
        return chain.invoke(input=kwargs)

    def reconfigure(self, prompt: PromptTemplate, **kwargs) -> dict:
        agent = ChatOpenAI(callbacks=self._callbacks, model=self.config.openai_api_model)
        output_parser = JsonOutputParser()
        chain = prompt | agent | output_parser
        return chain.invoke(input=kwargs)


def agent_executor(config: BasicLangChainConfig | LangChainConfigWithLangfuse):
    return LangChainExecutor(config=config)
