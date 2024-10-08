import os, sys
import dashscope
from dashscope import Generation
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from agents.team import Team


class Qwen:
    def __init__(self, config):
        pass

    def invoke(self, system_msg, user_msg):
        messages = [
            {"role": "system", "content": system_msg.content},
            {"role": "user", "content": user_msg.content},
        ]
        responses = Generation.call(
            "qwen-max",
            messages=messages,
            result_format="message",  
            stream=False,  
            # incremental_output=True,
        )
        return responses["output"]["choices"][0]["message"]["content"]


class GPT:
    def __init__(self, config: dict):
        self.model = ChatOpenAI(
            temperature=0.2,
            model=config["model"],
            api_key=config["api_key"],
            base_url=config["base_url"],
        )

    # args is HumanMessage, SystemMessage (variable length)
    def invoke(self, *args):
        # messages = [system_msg, user_msg]
        messages = [arg for arg in args]
        output_parser = StrOutputParser()

        chain = self.model
        result = chain.invoke(messages)

        Team.cost += result.response_metadata["token_usage"]["total_tokens"]
        Team.log.info(
            "following invoke cost: "
            + str(result.response_metadata["token_usage"]["total_tokens"])
            + " | all cost: "
            + str(Team.cost)
        )

        return result.content

    def invoke_MTurn(self, messages_list):
        output_parser = StrOutputParser()
        chain = self.model | output_parser
        result = chain.invoke(messages_list)
        return result

    def invoke_json(self, system_msg, user_msg):
        messages = [system_msg, user_msg]
        output_parser = JsonOutputParser
        chain = self.model | output_parser
        result = chain.invoke(messages)
        return result
