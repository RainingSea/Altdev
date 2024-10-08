import dashscope
from datetime import datetime
import argparse

from utils.commen import read_yaml
from agents.team import Team


# the __init__ of the agents folder has already imported the class, there's no need to write additional class import statements.
from agents import *
from model.model import Qwen, GPT

from langchain_openai import ChatOpenAI


def start_project():
    # framework execution start time
    start_time = datetime.now()

    # project initialization information
    project_name = "Code_Dependency_Analyzer"
    origin_req = "The Code Dependency Analyzer software analyzes code dependencies within a software project and provides a visual representation of the relationships between modules, classes, and functions. It helps developers understand how changes in one part of the code can impact other parts and identifies potential circular dependencies. The software can be implemented using static code analysis techniques without relying on external data sources."

    # Build Agent's Team
    team = Team()
    Team.project_name = project_name
    # set to absolute path for os.makedirs
    projdir = (
        "D:\\02-Project\\02-Align\\models\\altdev\\project_dir\\"
        + project_name
        + "\\"
    )
    Team.set_projdir(projdir)
    Team.set_log()

    # config for framework
    config = model_config()

    model = GPT(config["llm_4o"])
    model_review = GPT(config["llm_4o"])

    # launch project
    team.set_origin_req(project_name, origin_req)

    # 创建不同的角色
    product_manager = Product_Manager(llm=model, llm_review=model_review, team=team)
    architect = Architect(llm=model, llm_review=model_review, team=team)
    projct_manager = Project_Manager(llm=model, llm_review=model_review, team=team)
    programmer = Programmer(llm=model, llm_review=model_review, team=team)
    code_tester = Code_Tester(llm=model, llm_review=model_review, team=team)
    reviewer = Reviewer(target=projct_manager, team=team)

    team.hire_roles(
        product_manager, architect, projct_manager, programmer, code_tester, reviewer
    )
    #
    #
    # ------------------- launch project ------------------------
    team.run()
    # ------------------- launch project ------------------------
    #
    #
    # ------------------- Post Processing --------------------
    # statistics for this process(include team statistics and other information)
    # framework execution end time
    end_time = datetime.now()
    execution_time = end_time - start_time
    total_seconds = execution_time.total_seconds()
    milliseconds = int((total_seconds % 1) * 1000)
    milliseconds_str = str(milliseconds // 10).zfill(2)
    formatted_time = f"{int(total_seconds)}.{milliseconds_str}"
    Team.log.info(
        "\n-----------------\n"
        + team.log_project_stat()
        + "\n-------------------\n"
        + "Execute time: "
        + str(formatted_time)
        + " Seconds"
        + "\n-----------------"
    )
    # ------------------- Post Processing --------------------
    print(
        "\n-----------------\n"
        + team.log_project_stat()
        + "\n-------------------\n"
        + "Execute time: "
        + str(formatted_time)
        + " Seconds"
        + "\n-----------------"
    )


def model_config():
    # loading config for different models, include Qwen and GPT
    config = read_yaml("./0_config/config.yaml")
    dashscope.api_key = config["Qwen"]["api_key"]
    return config


if __name__ == "__main__":
    start_project()
