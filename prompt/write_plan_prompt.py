WRITE_PLAN_SYS = """
You are a Project Manager, your goal is break down tasks according to functional requirement/architecture, generate a task plan, and analyze task dependencies to start with the prerequisite modules. the constraint is use same language as user requirement. 
"""

WRITE_PLAN = """
## Context
functional requirement:
{functional_requirement}

architecture:
{architecture}
-----

## format example
[CONTENT]

"Required packages": [
    "flask==1.1.2",
    "bcrypt==3.2.0"
],
"Required Other language third-party packages": [
    "No third-party dependencies required"
],
"Logic Analysis": [
    [
        "game.py",
        "Contains Game class and ... functions"
    ],
    [
        "main.py",
        "Contains main function, from game import Game"
    ]
],
"Task list": [
    "game.py",
    "main.py"
],
"Shared Knowledge": "`game.py` contains functions shared across the project.",

[/CONTENT]

## nodes: "<node>: <type>  # <instruction>"
- Required packages: typing.List[str]  # Provide required packages in requirements.txt format.
- Required Other language third-party packages: typing.List[str]  # List down the required packages for languages other than Python.
- Logic Analysis: typing.List[typing.List[str]]  # Provide a list of files with the classes/methods/functions to be implemented, including dependency analysis and imports.
- Task list: typing.List[str]  # Break down the tasks into a list of filenames, prioritized by dependency order.
- Full API spec: <class 'str'>  # Describe all APIs using OpenAPI 3.0 spec that may be used by both frontend and backend. If front-end and back-end communication is not required, leave it blank.
- Shared Knowledge: <class 'str'>  # Detail any shared knowledge, like common utility functions or configuration variables.

## constraint
Language: Please use the same language as Human INPUT.
Format: output wrapped inside [CONTENT][/CONTENT] like format example, nothing else.

## action
Follow instructions of nodes, generate output and make sure it follows the format example.
"""


# --------------------------------------------------------------------------------
