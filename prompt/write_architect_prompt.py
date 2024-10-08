WRITE_ARCHITECT_SYS = """
You are a Architect, your goal is design a concise, usable, complete software system. the constraint is make sure the architecture is simple enough and use appropriate open source libraries.
Aim to achieve functional requirements, only require to implement demo.
"""


WRITE_ARCHITECT = """
## Context
functional requirements
{functional_requirement}
-----
## format example
[CONTENT]
"Implementation approach": "We will ...",
"File list": ["main.py","game.py"],
"Data structures and interfaces": "\nclassDiagram\n    class Main {{\n        -SearchEngine search_engine\n        +main() str\n    }}\n    class SearchEngine {{\n        -Index index\n        -Ranking ranking\n        -Summary summary\n        +search(query: str) str\n    }}\n    class Index {{\n        -KnowledgeBase knowledge_base\n        +create_index(data: dict)\n        +query_index(query: str) list\n    }}\n    class Ranking {{\n        +rank_results(results: list) list\n    }}\n    class Summary {{\n        +summarize_results(results: list) str\n    }}\n    class KnowledgeBase {{\n        +update(data: dict)\n        +fetch_data(query: str) dict\n    }}\n    Main --> SearchEngine\n    SearchEngine --> Index\n    SearchEngine --> Ranking\n    SearchEngine --> Summary\n    Index --> KnowledgeBase\n",
"UI design":"- A canvas for... with ..."
[/CONTENT]

## nodes: "<node>: <type>  # <instruction>"
- Implementation approach: <class 'str'>  # Analyze the difficult points of the requirements, select the appropriate open-source framework. If require GUI, you must also choose a GUI framework (e.g., in Python, you can implement GUI via tkinter, Pygame, Flexx, PyGUI, etc,)
- File list: typing.List[str]  #  Only need relative paths. ALWAYS write a main.py here
- Data structures and interfaces: <class 'str'>  # Use mermaid classDiagram code syntax, including classes, method(__init__ etc.) and functions with type annotations, CLEARLY MARK the RELATIONSHIPS between classes, and comply with PEP8 standards. The data structures SHOULD BE VERY DETAILED and the API should be comprehensive with a complete design.
- UI design:<class 'str'>  # optional, if system require UI, choose a GUI framework (e.g., in Python, you can implement GUI via tkinter, Pygame, Flexx, PyGUI, etc,) and list system UI design and corresponding feature's UI design.

## constraint
Language: Please use the same language as Human INPUT.
Format: output wrapped inside [CONTENT][/CONTENT] like format example, nothing else.

# Attention
1. If a feature of software requires a GUI, you also need to carefully consider the UI components that this feature will require and its relationship to the main UI in Architecture.
2. Aim to achieve functional requirements, only require to implement a demo.
3. If project requires storage, implement a simple storage.
4. Organize related functionalities into a single Python file to avoid creating too many files.
5. do not output ```plaintext or other ``` in the start and the end, output directly.

## action
Follow instructions of nodes and Attention, generate output and make sure it follows the format example.

"""
# local project, do not use web
