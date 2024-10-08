import os
import chardet

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from prompt.write_prd_prompt import WRITE_PRD, WRITE_PRD_SYS
# from prompt.review import (
#     PRD_REVIEW_ARCHITECT_COT,
#     PRD_REVIEW_TASK_PLAN_COT,
#     PRD_REVIEW_CODE_COT,
# )
from prompt.align_prompt import (
    PRD_REVIEW_ARCHITECTURE,
    PRD_REVIEW_PROJECT_PLAN,
    PRD_REVIEW_CODE,
)
from prompt.code_review import CODE_REVIEW
from agents.role import Role
from agents.team import Team
from messages.message import Message
from datetime import datetime, timedelta

from utils.commen import write_to_file


class Product_Manager(Role):
    name: str = "Pole"
    profile: str = "Product Manager"
    team: Team = None
    llm: object
    llm_review: object
    system_msg: str = WRITE_PRD_SYS
    own_message: Message = None
    review_prompt: dict[str, str] = {
        "Architect": PRD_REVIEW_ARCHITECTURE,
        "Project Manager": PRD_REVIEW_PROJECT_PLAN,
        "Programmer": PRD_REVIEW_CODE,
    }
    review_code_prompt: str = CODE_REVIEW
    action: str = "functional requirement document"

    def go(self):
        print(self.profile + " " + self.name + " generate PRD......")
        Team.log.info(self.profile + " " + self.name + " Writing PRD...")

        # ---------- get the information needed from SCR ----------
        original_requirement = self.getOriginRequirement().content

        # ---------- LLM ----------
        # ---------- constructing prompt to LLM ----------
        system_prompt = SystemMessage(content=WRITE_PRD_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_PRD)
        user_prompt_msg = user_prompt_template.invoke(
            {"original_requirement": original_requirement}
        )
        user_prompt = user_prompt_msg.to_messages()[0]
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        # prompt LLM
        result = self.llm.invoke(system_prompt, user_prompt)

        # ---------- logging -----------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        prd_msg = Message(sender=self.profile, content=result)
        self.own_message = prd_msg

        Team.all_messages.append(prd_msg)
        # ---------- writing result to local ----------
        self.message_to_file(prd_msg.content)

        return

    def message_to_file(self, msg_content):
        # # ---------- writing PRD to local ----------
        file_name = "prd.md"

        # log.info(self.profile + " writting PRD")
        super().save_file_overwrite(Team.project_dir + file_name, msg_content)

    def update_own_message(self, msg: Message):
        self.own_message = msg
        Team.all_messages[1] = msg

    def get_team_roles(self):
        return self.team.get_team_roles()

    def getOriginRequirement(self):
        return Team.all_messages[0]

    def setSuggestion(self, suggestion):
        self.suggestion = suggestion

    def clearSuggestion(self):
        self.suggestion = ""

    def test(self):
        Team.arthur_talk(self)
