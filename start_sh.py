import dashscope
from datetime import datetime
import argparse

from utils.commen import read_yaml
from agents.team import Team


# # the __init__ of the agents folder has already imported the class, there's no need to write additional class import statements.
from agents import *
from model.model import Qwen, GPT

from langchain_openai import ChatOpenAI

# this file contains the starting point of the project. please use a Python script to run this file to start the project.
# this file involves configurations and does not cover specific processes, which are detailed in the team.py.


def start_project():
    parser = argparse.ArgumentParser(description="original Requirement")

    parser.add_argument("--name", type=str, help="Name")
    parser.add_argument("--project", type=str, help="original Requirement")

    args = parser.parse_args()
    print(f"Received Original Requirement Name : {args.name}")
    print(f"Received Original Requirement : {args.project}")

    project_name = args.name
    origin_req = args.project

    # framework execution start time
    start_time = datetime.now()

    # project initialization information
    # project_name = "Headlinr"
    # origin_req = "Headlinr is a news software application that provides personalized news summaries. It uses natural language processing techniques to extract key information from news articles and generates concise summaries. Users can customize their news preferences, including topics and sources they are interested in. The software employs a ranking algorithm to prioritize the most relevant news based on user preferences. It also supports bookmarking and sharing features. Headlinr aims to provide a streamlined and personalized news browsing experience. Implemented using Python."

    # Build Agent's Team
    team = Team()
    Team.project_name = project_name
    Team.align_check_num = 1
    Team.mad_num = 1

    # set to absolute path for os.makedirs
    projdir = (
        "D:\\02-Project\\02-Align\\models\\altdev\\project_dir\\" + project_name + "\\"
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
