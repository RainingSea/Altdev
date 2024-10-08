from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

from prompt.write_architect_prompt import WRITE_ARCHITECT_SYS, WRITE_ARCHITECT
from prompt.align_prompt import ARCHITECTURE_REVIEW_PROJECT_PLAN, ARCHITECTURE_CODE
from agents.role import Role
from agents.team import Team
from messages.message import Message


class Architect(Role):
    name: str = "Arnold"
    profile: str = "Architect"
    llm: object
    llm_review: object
    system_msg: str = WRITE_ARCHITECT_SYS
    own_message: Message = None
    team: Team = None
    review_prompt: dict[str, str] = {
        "Project Manager": ARCHITECTURE_REVIEW_PROJECT_PLAN,
        "Programmer": ARCHITECTURE_CODE,
    }
    action: str = "Architecture"

    def getMessage():
        pass

    def go(self):
        print(self.profile + " " + self.name + " generate Architect......")
        Team.log.info(
            self.profile + " " + self.name + " generate System Architect......"
        )

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content

        # ---------- constructing prompt to LLM ----------
        # using message template from LangChain, the result is SYS Message & HUMAN Message.
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_ARCHITECT)
        user_prompt_msg = user_prompt_template.invoke(
            {"functional_requirement": functional_requirement}
        )
        user_prompt = user_prompt_msg.to_messages()[0]

        system_prompt = SystemMessage(content=self.system_msg)

        # ---------- prompt LLM ----------
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        result = self.llm.invoke(system_prompt, user_prompt)

        # ------------ logging ----------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        Team.all_messages.append(module_msg)

        # ---------- writing result to local ----------
        self.message_to_file(module_msg.content)

        return

    def update_own_message(self, msg: Message):
        self.own_message = msg
        Team.all_messages[2] = msg

    def message_to_file(self, msg_content):
        # ---------- writing Architecture to local ----------
        file_name = "architect.md"

        Team.log.info(self.profile + " writting ARCHITECT")
        super().save_file_overwrite(Team.project_dir + file_name, msg_content)

    def getOriginRequirement(self):
        return Team.all_messages[0]

    def getPRD(self):
        return Team.all_messages[1]
