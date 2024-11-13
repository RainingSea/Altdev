import re
import json


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage


from agents.role import Role
from agents.team import Team
from prompt.align_prompt import REGENERATE, RETHINK, COMPLEMENT, ALIGN_WITH_WHO
from messages.message import Message


# ---------- align process ----------
# workflow of alignment
# role: proposer of alignment
# team: proposer's team, to which participant role belongs
def arthur_talk(role: Role, team: Team):
    whether_align = False
    # - Log original content that needs to be aligned
    Team.log.info("Begin Check for " + role.profile)

    # - get team's active roles and let everyone check result
    all_roles = Team.get_active_roles()

    print("role involved in Alignment Checking: " + str(all_roles))
    Team.log.info("role involved in Alignment Checking: " + str(all_roles))

    # init align_result
    align_result = role.own_message.content

    # ------------ check roles to align ----------------
    print("[1] Roles go to Check")
    Team.log.info("[1] Roles go to Check")

    align_talk_turn = 1
    MAX_ALIGN_TURN = Team.align_check_num

    while align_talk_turn <= MAX_ALIGN_TURN:
        print("Begin the " + str(align_talk_turn) + " turn Alignment")
        Team.log.info("\nBegin the " + str(align_talk_turn) + " turn Alignment")

        align_roles = []
        check_result_msg = []

        # [1] Alignment Checking
        for i in range(len(all_roles)):
            align_participant_msg = (
                ChatPromptTemplate.from_template(
                    team.roles[all_roles[i]].review_prompt[role.profile]
                )
                .invoke(
                    {
                        "participant_content": team.roles[
                            all_roles[i]
                        ].own_message.content,
                        "role_content": align_result,
                    }
                )
                .to_messages()[0]
            )
            # align prompt
            Team.log.info(
                team.roles[all_roles[i]].profile
                + " Align check prompt: "
                + align_participant_msg.content
            )
            # record align check result
            participant_suggestion = team.roles[all_roles[i]].llm.invoke(
                align_participant_msg
            )
            print(
                "Align | "
                + team.roles[all_roles[i]].profile
                + " | check result is :  \n"
                + participant_suggestion
            )
            Team.log.info(
                "Align | "
                + team.roles[all_roles[i]].profile
                + " | check result is: \n"
                + participant_suggestion
            )

            # role reporting problem will be list in align roles, participant in MAD process
            # After Check, We get { align_roles & check_result }
            participant_suggestion_msg = Message(
                sender=team.roles[all_roles[i]].profile,
                content=participant_suggestion,
            )
            if "[NOTMATCH]" in participant_suggestion:
                align_roles.append(team.roles[all_roles[i]].profile)
                check_result_msg.append(participant_suggestion_msg)
            elif "[MATCH]" in participant_suggestion:
                pass
                # align_roles.append(team.roles[all_roles[i]].profile)
                # check_result_msg.append(participant_suggestion_msg)
            else:
                # In case LLM does not output [MATCH] or [NOTMATCH]
                align_roles.append(team.roles[all_roles[i]].profile)
                check_result_msg.append(participant_suggestion_msg)

        print("After Checking, Group Roles are: " + str(align_roles))
        Team.log.info("After Checking, Group Roles are: " + str(align_roles))

        # [1-1] if all roles no problem, align finished
        if len(align_roles) == 0:
            # if all roles check result is GOOD, then return
            if align_talk_turn == 1:
                # if all roles check result is GOOD in first align, then return original
                Team.log.info("All roles no problem in Checking, No Align")
                whether_align = False
                return whether_align, align_result
            else:
                # if all roles check result is GOOD, then return
                Team.log.info("After Align, All roles no problem in Checking, No Align")
                whether_align = True
                return whether_align, align_result

        # [1-2] at least one role misalign, enter MAD-S / MAD-M

        sup_turn = 1
        MAX_SUP_TURN = Team.mad_num

        # copy check_result_msg because MAD needs to change.
        raw_complement_suggestion = []
        for _r in check_result_msg:
            raw_complement_suggestion.append(_r)

        while sup_turn <= MAX_SUP_TURN:
            # MAD-S / MAD-M
            # whether to supplement role's own messages based on messages from other roles.
            print("\nBegin the " + str(sup_turn) + " turn Supplement(MAD) ")
            Team.log.info("\nBegin the " + str(sup_turn) + " turn Supplement(MAD) ")

            # MAD-S / special case where there is only one role
            if len(align_roles) <= 1:
                Team.log.info("Only one roles in Align, no MAD")
                break
            else:
                # if there's more than 2 agents in align team, discussion
                _raw_complement_suggestion = []
                for j in range(len(align_roles)):
                    # extract other's message
                    other_suggestion = []
                    self_suggestion = None
                    for msg in raw_complement_suggestion:
                        if msg.sender != team.roles[align_roles[j]].profile:
                            other_suggestion.append(msg)
                        else:
                            self_suggestion = msg

                    # supplement one's own check result based on others' check result

                    complement_align_participant_msg = (
                        ChatPromptTemplate.from_template(COMPLEMENT)
                        .invoke(
                            {
                                "participant_role": team.roles[align_roles[j]].profile,
                                "role_action": role.action,
                                "participant_action": team.roles[align_roles[j]].action,
                                "participant_content": team.roles[
                                    align_roles[j]
                                ].own_message.content,
                                "role_content": align_result,
                                "participant_review": self_suggestion.content,
                                "other_review": read_suggestion(other_suggestion),
                            }
                        )
                        .to_messages()[0]
                    )
                    # supplement prompt
                    Team.log.info(
                        team.roles[align_roles[j]].profile
                        + " complement self's review prompt: \n"
                        + complement_align_participant_msg.content
                    )
                    # record supplement thinking result
                    complement_align_participant_suggestion = team.roles[
                        align_roles[j]
                    ].llm.invoke(complement_align_participant_msg)
                    Team.log.info(
                        team.roles[align_roles[j]].profile
                        + " complement result is \n"
                        + complement_align_participant_suggestion
                    )

                    if "[NOT_NEED]" in complement_align_participant_suggestion:
                        temp_review = self_suggestion
                    else:
                        temp_review = Message(
                            sender=team.roles[align_roles[j]].profile,
                            content=complement_align_participant_suggestion,
                        )
                    _raw_complement_suggestion.append(temp_review)
                raw_complement_suggestion = []
                for _r in _raw_complement_suggestion:
                    raw_complement_suggestion.append(_r)
                sup_turn = sup_turn + 1

        # filter the MAD results, assuming there might be changes.
        # and determine flag
        flag_suggestion = []
        complement_suggestion = []
        complement_suggestion_string = ""

        for i in range(len(raw_complement_suggestion)):
            if "[NOTMATCH]" in raw_complement_suggestion[i].content:
                flag_suggestion.append("BAD")
                complement_suggestion.append(raw_complement_suggestion[i])
                complement_suggestion_string += (
                    team.roles[align_roles[i]].profile
                    + ": "
                    + raw_complement_suggestion[i].content
                    + "\n"
                )
            elif "[MATCH]" in raw_complement_suggestion[i].content:
                flag_suggestion.append("GOOD")
                complement_suggestion_string += (
                    team.roles[align_roles[i]].profile
                    + "init review: "
                    + "No problem \n"
                )
            else:
                flag_suggestion.append("BAD")
                complement_suggestion.append(raw_complement_suggestion[i])
                complement_suggestion_string += (
                    team.roles[align_roles[i]].profile
                    + ": "
                    + raw_complement_suggestion[i].content
                    + "\n"
                )

        # ---------- MASTER or CODE decide whether to approve it. ----------
        # Logically, if roles reache this step, it means all NOTMATCH, so they should not pass.
        # will correct here after releasing.
        Team.log.info("flag " + str(flag_suggestion))
        PASS = True
        for i in range(len(flag_suggestion)):
            if flag_suggestion[i] != "GOOD":
                PASS = False
                break

        # decide whether to modify or end the alignment based on the results from the Agents (which may include humans).
        if PASS == False:
            whether_align = True
            # extract the not align check result to reduce context length

            user_prompt_template_1 = ChatPromptTemplate.from_template(RETHINK)
            code_review_user_msg_1 = user_prompt_template_1.invoke(
                {
                    "result": read_suggestion(complement_suggestion),
                }
            )
            code_review_user_prompt_1 = code_review_user_msg_1.to_messages()[0]

            Team.log.info("Extract prompt is: \n" + code_review_user_prompt_1.content)
            p_result = role.llm.invoke(code_review_user_prompt_1)
            Team.log.info("Extracted review result is: " + p_result)

            role_msg = (
                ChatPromptTemplate.from_template(REGENERATE)
                .invoke(
                    {
                        "role": role.profile,
                        "suggestion": p_result,
                        "role_action": role.action,
                        "role_content": align_result,
                    }
                )
                .to_messages()[0]
            )
            Team.log.info(
                role.profile + " regenerating content based on review result......"
            )
            Team.log.info(role_msg.content)
            align_llm_result = role.llm.invoke(role_msg)
            print(align_llm_result)
            Team.log.info("Aliged result is: \n" + align_llm_result)
            align_result = align_llm_result
            align_talk_turn = align_talk_turn + 1
        else:
            # never reached [need fix after release]
            print("all Align, alignment finished")
            Team.log.info("Everyone Reaches an agreement, Align is Done")
            return False, align_result

    Team.log.info("Align is upon MAX, return")
    whether_align = True
    return whether_align, align_result


# only read messages from others and not self own messages
def read_msg(profile, messages, team):
    result = ""
    for msg in messages:
        if msg.sender != profile:
            result = (
                result
                + "# "
                + msg.sender
                + " - "
                + team.roles[msg.sender].action
                + "\n"
                + msg.content
                + "\n"
            )
    return result


def read_suggestion(suggestion):
    # accept a Message List
    # return a more friendly result(String type)
    # User's review: xxx, User's review xxx
    result = ""
    for msg in suggestion:
        result = result + "[ " + msg.sender + "'s review: " + msg.content + " ]\n"
    return result


def str_to_role(str_role_list):
    """ """
    f = re.findall("[\[](.*?)[\]]", str_role_list)
    for role_profile in f:
        try:
            print(role_profile)
        except:
            print("Error role：" + role_profile)
    return f
