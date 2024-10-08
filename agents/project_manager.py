# langchain lib
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# custom lib
from prompt.write_plan_prompt import WRITE_PLAN_SYS, WRITE_PLAN
from prompt.align_prompt import TASK_PLAN_REVIEW_CODE
from agents.role import Role
from agents.team import Team
from messages.message import Message


class Project_Manager(Role):
    name: str = "Tsunade"
    profile: str = "Project Manager"
    llm: object
    llm_review: object
    system_msg: str = WRITE_PLAN_SYS
    own_message: Message = None
    team: Team = None
    review_prompt: dict[str, str] = {"Programmer": TASK_PLAN_REVIEW_CODE}
    action: str = "Task Plan"

    def go(self):
        print(self.profile + " " + self.name + " generate Project Plan......")
        Team.log.info(self.profile + " " + self.name + " generate Project PLAN......")

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        architect = self.getSystemModule().content

        # ---------- constructing prompt to LLM ----------
        # using message template from LangChain, the result is SYS Message & HUMAN Message.
        system_prompt = SystemMessage(content=WRITE_PLAN_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_PLAN)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "functional_requirement": functional_requirement,
                "architecture": architect,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        # prompt LLM
        result = self.llm.invoke(system_prompt, user_prompt)

        # ---------- logging --------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        plan_msg = Message(sender=self.profile, content=result)
        self.own_message = plan_msg

        Team.all_messages.append(plan_msg)
        # ---------- writing result to local ----------
        self.message_to_file(plan_msg.content)

        return

    def update_own_message(self, msg: Message):
        self.own_message = msg
        Team.all_messages[3] = msg

    def message_to_file(self, msg_content):
        # ---------- writing Code Plan(Task Plan) to local ----------
        file_name = "task plan.md"

        Team.log.info(self.profile + " writting TASK PLAN")
        super().save_file_overwrite(Team.project_dir + file_name, msg_content)

    def getOriginRequirement(self):
        return Team.all_messages[0]

    def getPRD(self):
        return Team.all_messages[1]

    def getSystemModule(self):
        return Team.all_messages[2]
