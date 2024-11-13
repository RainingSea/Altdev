from agents.role import Role
from agents.team import Team
from pathlib import Path
import sys, os, subprocess

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from prompt.write_code_prompt import DEBUG, CODING_SYS
from messages.message import Message


class Code_Tester(Role):
    name: str = "Tesla"
    profile: str = "Code Tester"
    team: Team = None
    own_message: Message = None

    def go(self):
        # test main.py or app.py (can not test Flask project, Flask project requires manual testing)
        architecture = self.getArchiture().content
        if "flask" in architecture.lower():
            Team.log.info(
                "Tester | ----------- Use flask, please test by human --------------------"
            )
            test_msg = Message(sender=self.profile, content="Test Stop")
            self.own_message = test_msg
            Team.all_messages.append(test_msg)
            return

        test_turn = 1
        install_turn = 1
        Max_test_turn = 1 
        Max_install_turn = 3
        
        while test_turn <= Max_test_turn and install_turn <= Max_install_turn:
            main_py_path = self.get_entry_file()
            print(main_py_path)
            # test code
            result, result_data = self.run_main_py(main_py_path)
            if result == "SUCCESS":
                test_msg = Message(sender=self.profile, content="Test Success")
                self.own_message = test_msg
                Team.all_messages.append(test_msg)
                break
            elif result == "IMPORT_ERROR":
                Team.log.info("Tester | lacking third package:" + result_data)
                install_result = self.install_package(result_data)
                if install_result == "INS_S":
                    print(
                        "Tester | Restarting the execution after installing the missing package."
                    )
                    Team.log.info(
                        "Tester | Restarting the execution after installing the missing package."
                    )
                    install_turn += 1
                else:
                    # print("Tester | Install failed(experied time / error)")
                    # Team.log.info("Tester | Install failed(experied time / error)")
                    test_msg = Message(
                        sender=self.profile, content="Test Install Failed"
                    )
                    self.own_message = test_msg
                    Team.all_messages.append(test_msg)
                    break
            elif result == "OTHER_ERROR":
                # Coding Error, call the Coder to fix
                print(f"An error occurred: {result_data}")
                Team.log.info("Tester | An error occurred: " + result_data)

                code = self.getCode().content
                system_prompt = SystemMessage(content=CODING_SYS)
                user_prompt_template = ChatPromptTemplate.from_template(DEBUG)
                user_prompt_msg = user_prompt_template.invoke(
                    {
                        "code": code,
                        "error_report": result_data,
                    }
                )
                user_prompt = user_prompt_msg.to_messages()[0]
                Team.log.info(system_prompt.content + "\n" + user_prompt.content)
                fix_code_result = self.team.roles["Programmer"].llm.invoke(
                    system_prompt, user_prompt
                )

                # logging
                Team.log.info(
                    "Tester | Fixed code based on the test :\n" + fix_code_result
                )
                self.team.roles["Programmer"].update_own_message(
                    Message(sender="Programmer", content=fix_code_result)
                )
                self.team.roles["Programmer"].message_to_file_test(fix_code_result)
                # Re-test the fixed code, but only record the results without processing them.
                self.run_main_py(main_py_path)
                test_turn += 1
        # If not exit from the while loop, it must be following two situations, which necessarily means there is an error
        test_msg = Message(sender=self.profile, content="Test Still Failed")
        self.own_message = test_msg
        Team.all_messages.append(test_msg)

    def get_entry_file(self):
        # windows use \\ as path separator
        # Linux use / as path separator
        if Path(Team.project_dir + "test_code\\main.py").exists():
            entry_file = Team.project_dir + "test_code\\main.py"
        elif Path(Team.project_dir + "test_code\\app.py").exists():
            entry_file = Team.project_dir + "test_code\\app.py"
        elif Path(Team.project_dir + "review_code\\main.py").exists():
            entry_file = Team.project_dir + "review_code\\main.py"
        elif Path(Team.project_dir + "review_code\\app.py").exists():
            entry_file = Team.project_dir + "review_code\\app.py"
        elif Path(Team.project_dir + "code\\main.py").exists():
            entry_file = Team.project_dir + "code\\main.py"
        elif Path(Team.project_dir + "code\\app.py").exists():
            entry_file = Team.project_dir + "code\\app.py"
        else:
            return
        return entry_file

    # def write_code(self, repaired_code):
    #     self.team.roles["Programmer"].message_to_file_test(repaired_code)

    def run_main_py(self, main_py_path):
        """Execute the main.py file from the specified directory."""
        try:
            # Execute the main.py script with a timeout
            process = subprocess.Popen(
                [sys.executable, main_py_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                # Wait for a specified time or until the process completes
                stdout, stderr = process.communicate(
                    timeout=2
                )  # Adjust timeout as needed
                normal_exit = True
            except subprocess.TimeoutExpired:
                # Process is still running after timeout, terminate it
                process.terminate()
                stdout, stderr = (
                    process.communicate()
                )  # Fetch any remaining output after termination
                normal_exit = False

            # Decode output and error
            stdout = stdout.decode()
            stderr = stderr.decode()

            if normal_exit and process.returncode == 0:
                print("Program executed successfully with no errors.")
                Team.log.info("Tester | Program executed successfully with no errors.")
                return "SUCCESS", None
            elif not normal_exit:
                print(
                    "Process terminated due to timeout, which is considered as normal execution."
                )
                Team.log.info(
                    "Tester | Process terminated due to timeout, which is considered as normal execution."
                )
                return "SUCCESS", None
            else:
                print(f"Error: {stderr}")
                Team.log.info("Tester | Error: " + stderr)
                if "No module named" in stderr:
                    missing_package = (
                        stderr.split("No module named")[-1].strip().replace("'", "")
                    )
                    return "IMPORT_ERROR", missing_package
                else:
                    return "OTHER_ERROR", stderr

        except Exception as e:
            return "OTHER_ERROR", str(e)

    def install_package(self, package_name):
        """Install the missing package."""
        print(f"Installing missing package: {package_name}")
        Team.log.info("Installing missing package: " + package_name)
        try:
            # using subprocess & timeout
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                timeout=120, # timeout
                check=True,  # throw CalledProcessError if failed
            )
        except subprocess.TimeoutExpired:
            print(f"\nInstallation of {package_name} timed out after 120 seconds.")
            Team.log.info(
                "Tester | Installation of "
                + package_name
                + " timed out after 120 seconds."
            )
            return "INS_E"
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package_name}. Error: {e}")
            Team.log.info("Tester| Failed to install " + package_name)
            return "INS_E"
        else:
            if result.returncode == 0:
                print(f"Tester | {package_name} installed successfully.")
                Team.log.info(package_name + " installed successfully.")
            return "INS_S"

    def getArchiture(self):
        return Team.all_messages[2]

    def getCode(self):
        return Team.all_messages[4]
