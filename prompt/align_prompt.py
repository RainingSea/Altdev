# Agent looking for which other Agents to align
ALIGN_WITH_WHO = """
I am {role} in a software engineering project team, and the other role of the project team has generated the following content:
{other_rule_content}

I have generated a {role_action}, content is {role_content}, and I'm wonder who(other than myself) in software team roles should review my content. 
So from software team roles :{roles_list}, Output which roles, other than myself, I need to discussion with (can be more than one role)? 

# Rules
(1) your answer should only from the given software team roles:[{roles_list}], but without {role}, and do not answer role that does not exist in software team roles;
(2) consicely output your result like format, do not need to explain your reason. 
(3) do not use ``` in the beginning to illustrate json file, only output a pure json result.

-----
# Format Example
{{"roles":["role1","role2","role3",...]}}.
-----
Must output a json follow Format Example, consicely output your result following Format Example, do not need to explain your reason.
"""


# ------------------------------------
# Product Manager Review Prompts
PRD_REVIEW_ARCHITECTURE = """
You are a Product Manager.
This is a Requirement Document:
{participant_content}

This is a Architecture:
{role_content}

-----
Example:
## example for not match
Requirement Document:
---
2.3. The system shall allow users to choose the shape of the sticker (e.g., circle, square, custom shape).

Architecture:
class ImageEditor {{
        +upload_image(file_path: str) Image
        +add_decorative_elements(image: Image, element: str, position: tuple) Image
        +save_image(image: Image, file_path: str) void
    }}
# Not match. The architecture does not explicitly mention the function of selecting shapes. need to add relevant methods in the ImageEditor class and add a shape selection menu in the GUI class.
---
......

final Summary: [NOTMATCH]

## example for match
Requirement Document:
---
2.5. The system shall allow users to add text to the sticker.

Architecture:
+add_text(image: Image, text: str, position: tuple, font: str, size: int, color: str) Image
# match. add_text() mention requirement of add text to the sticker.
---
....

**final summary: [MATCH]**

------

# Action
Analyze whether all the functions in the requirements are match in the architecture(such as Class and Function).
Add a summary for each analysis, whether it is match or not. use --- to separate each requirement check.
In the final summary, output whether it is MATCH or NOTMATCH(warpped in [], [MATCH] for MATCH summary and [NOTMATCH] for NOTMATCH summary).
Only output [MATCH] or [NOTMATCH] in final summary based on your analysis.
Follow Example and output your result.
"""

PRD_REVIEW_PROJECT_PLAN = """
You are a Product Manager.
This is a Requirement Document:
{participant_content}

This is a Task Plan:
{role_content}
------
# Example
## example for not match
---
The system shall allow users to create 3 tools include pencil, brush and spray gun.
    ...
    [
        "brush.py",
        "Contains various brushes to let user select."
    ]
    ...
# Not match. Requirement to create three types of brushes lost, need to point out the various brush types include pencil, brush, spary gun. 
---
......

**final Summary: [NOTMATCH]**

## example match
---
The system shall allow users to create 3 tools include pencil, brush and spray gun.
    ...
    [
        "brush.py",
        "Contains 3 types of brushes(pencil, brush, spary gun) to let user select."
    ]
    ...
# match.
---
......

**final Summary: [MATCH]**
------

# Instruction
(1)Each file name in the Logic Analysis is followed by the description that the file is responsible for. These files do not have code yet, so you only need to judge from these functional descriptions.
(2)File description in the Task List must accurately and completely match the requirement it is responsible for. Otherwise it's summary is NOTMATCH.

# Action
Carefully analyze whether each feature in the requirements is correctly and accurately described by Logic Analysis in task plan.
Add a summary after each analysis, whether it is match or not. use --- to separate each requirement check.
In the final summary, output whether it is MATCH or NOTMATCH(warpped in [], output [MATCH] for MATCH summary and [NOTMATCH] for NOTMATCH summary).
"""

PRD_REVIEW_CODE = """
Verify that the code implements the intended functionality without omissions or errors.
Perform logical checks to ensure the code is correct and sound.

# Context
## functional requirement
{participant_content}

## Code
{role_content}

-----
# Format Example 1
Let's evaluate the provided code against the specified functional requirements:

1. Users can select their own photo as the base image for the sticker):
Implemented: Yes, the upload_image method allows users to select and upload an image.
Meets Requirements: Yes, it fully meets the requirement by enabling image upload.
...

**[SUMMARY:MATCH]**

# Format Example 2
Let's evaluate the provided code against the specified functional requirements:

1. Users can select their own photo as the base image for the sticker):
Implemented: No, the upload_image method is not ...
Meets Requirements: Partially, it doesn't meets the requirement that enabling image upload.
...

**[SUMMARY:NOTMATCH]**
-----

# Instructions
above content is a functional requirements of a software and the code of this software. 
Carefully judge whether the software has implemented these functions one by one according to the key points of the functional requirements. 
step by step to judge whether the functions are implemented, first, whether the code has tried to implement these functions. Second, if it has tried to implement these functions, whether the code can fully meet the functional requirements in implementation.
if a function's code contain pass, placeholder, or leave for future implementation, consider it "not match" and explain reason.

output a final summary in last, [SUMMARY:MATCH] for all match result, [SUMMARY:NOTMATCH] for not match or partilly match result.

# Action
Follow instruction, generate review output and make sure follows one of the format example.
"""

# ------------------------------------
# Architect Review Prompts
ARCHITECTURE_REVIEW_PROJECT_PLAN = """
You are a An software Architect.
# Architecture
{participant_content}
# Task PLan
{role_content}
-----
# Action
Carefully analyze whether the technology stack used in the task Plan conforms to the architecture, and whether the relationships between files are consistent with the architecture design.
In the final summary, output whether it is MATCH or NOTMATCH(warpped in [], output [MATCH] for MATCH summary and [NOTMATCH] for NOTMATCH summary).
"""

ARCHITECTURE_CODE = """
You are a An software Architect.
# Context
## Architecture
{participant_content}
## Code
{role_content}
------
# Example
## example for not match
technology stack: ...
class & function check: ....
GUI design: ...
file relationship: ...

**final Summary: [SUMMARY:NOTMATCH]**
--
## example for match
technology stack: ...
class & function check: ....
file relationship: ...
UI design: ...

**final Summary: [SUMMARY:MATCH]**

-----
# Action
(1)Carefully review whether the technology stack used in each code file belongs to the architecture.
(2)Carefully review whether each item in "Data structures and interfaces" have correctly code implementations(code cannot contain pass, placeholder, cannot be left for future implementation).
(3)Carefully review whether the reference relationship between files and class, functions and variables is consistent with architecture.
(4)If the system has a GUI, Carefully check whether there are corresponding GUI components for the functions that use the GUI, and whether these components are appropriately shown in UI.
In the final summary, output whether it is MATCH or NOTMATCH(warpped in [], output [SUMMARY:MATCH] for MATCH summary and [SUMMARY:NOTMATCH] for NOTMATCH summary).
"""

# ------------------------------------
# Project Review Prompts
TASK_PLAN_REVIEW_CODE = """
You are a An software Project Manager.
# Context
## Task Plan
{participant_content}
## Code
{role_content}
------
# Example
## example for not match
---
Task:
"health_profile.py",
"Contains HealthProfileManager class with methods to create, update, and retrieve health profiles."
Code:
Implemented: no, the create method in healthy_profile.py is not implement by code. 
Implemented: no, the create method need a button to trigger but no code implementation.
---
...

**final Summary: [SUMMARY:NOTMATCH]**
---
...

## example for match
---
Task:
"health_profile.py",
"Contains HealthProfileManager class with methods to create, update, and retrieve health profiles."
Code:
Implemented: yes, the create method in healthy_profile.py is implement by code, user can input their profile. 
(optional if required ) GUI Implemented: Yes, the main UI has a button to trigger create function.
---
...

**final Summary: [SUMMARY:MATCH]**

-----
# Action
step by step, Carefully analyze whether each file in the code contains code that fully implements the all functionality or description defined by the file with the same name in the Logic Analysis in Task Plan.
output [SUMMARY:NOTMATCH] because code can not contain pass, placeholder, can not be left for future implementation.
In the final summary, summary previous result and output whether MATCH or NOTMATCH(warpped in [], output [SUMMARY:MATCH] for MATCH summary and [SUMMARY:NOTMATCH] for NOTMATCH summary).

"""

COMPLEMENT = """
You are {participant_role}, You are reviewing a {role_action} based on your content.
You have generated your review result based on your {participant_action}, and others have also generated review result, All of you are in a team.

---
# Context
## {participant_action}
{participant_content}
## {role_action}
{role_content}

# Review Result
## Your original review result
{participant_review}
## other's review result
{other_review}

# Action
First, you need to carefully analyze other's review result of {role_action} and your review result.
Second, Using other's review result as reference, based on your {participant_action}, you need to regenerate a new review result of the {role_action}.

# Constraint
(1)format of Regenerated result must carefully follow your original review result' format.
(2)no need to copy others' opinions directly.
(2)Do not need to explain in the start and end.
(3)Do not add such as "Regenerated Review Result" in the start.
"""


RETHINK = """These are raw outputs from different roles. 
step by step, Extract the not match or Partially match content from these roles's raw outputs, along with the context surrounding each negative statement.
After extracting the content, the role of the output should still be preserved.
# Example
## Raw Output: 
[ Product Manager's review: Requirement Document:
...
---
2.6. The system shall allow users to set reminders for their meditation sessions.

Architecture:
- Settings View: Allows setting reminders and managing user preferences.
# match. The Settings View in the UI design includes functionality for setting reminders.
---
2.7. The system shall provide users with the ability to mark meditation sessions as completed.

Architecture:
- The architecture does not explicitly mention marking sessions as completed.
# not match. There is no explicit function or method for marking sessions as completed in the architecture.
---
...

## Extracted Result
[ Product Manager's review: Requirement Document:
---
2.7. The system shall provide users with the ability to mark meditation sessions as completed.

Architecture:
- The architecture does not explicitly mention marking sessions as completed.
# not match. There is no explicit function or method for marking sessions as completed in the architecture.
---
...

# raw output:
{result}

# Instruction
step by step, Extract the not match or Partially match content from these roles's raw outputs, along with the context surrounding each negative statement.
After extracting the content, the role of the output should still be preserved.

follow Instruction, only do extracting, do not need to explain.
"""

# PRD_ESSENCE_MAKE = """
# You are a requirements analyst reviewing a piece of code.
# you have provided your suggestion. Others have also provided their suggestion.
# From a requirements perspective, you need to review these opinions to see if you
# """


# ------------------------------------
REGENERATE = """
You are {role} in a software team.

# Context

## Problem
{suggestion}

## Previous {role_action}
{role_content}

-----
Based on the previous {role_action}, fix the Problem and regenerate your {role_action}.
first, you should analyze the problem; 
second, you should think about how to solve the problem; 
third, based on your thinking, you should regenerate your {role_action}, but the format of regenerated {role_action} should follow previous.

Refer to each item and corresponding format of the previous {role_action}, and output a new {role_action}.
Do not include the Problem in your refined output.
Only output regenerated or updated content, do not explain reason.
"""
