import os
from pydantic import Field

# langchain lib
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# custom lib
from prompt.write_code_prompt import CODING_SYS, CODING
from agents.role import Role
from agents.team import Team
from messages.message import Message
from align_flow.align_flow import arthur_talk

class Reviewer(Role):
    name: str = "Rox"
    profile: str = "Reviewer"
    target: Role
    team: Team

    def set_review_target(self, role: Role):
        self.target = role

    def go(self):
        # align process to target role
        # add a align flag
        result_flag, result = arthur_talk(self.target, self.target.team)
        if result_flag:
            # After alignment finished, replace the content of the target role with the updated file and rewrite the local files.
            self.target.message_to_file(result)
            self.target.update_own_message(
                Message(sender=self.target.profile, content=result)
            )
        return
