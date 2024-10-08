CODE_REVIEW = """
Verify that the code implements the intended functionality without omissions or errors.
Perform logical checks to ensure the code is correct and sound.

# Context
## functional requirement
{own_content}

## Code
{codes}

-----
# Format Example 1
Let's evaluate the provided code against the specified functional requirements:

1. Users can select their own photo as the base image for the sticker):
Implemented: Yes, the upload_image method allows users to select and upload an image.
Meets Requirements: Yes, it fully meets the requirement by enabling image upload.
...

[SUMMARY:MATCH]

# Format Example 2
Let's evaluate the provided code against the specified functional requirements:

1. Users can select their own photo as the base image for the sticker):
Implemented: No, the upload_image method is not ...
Meets Requirements: Partially, it doesn't meets the requirement that enabling image upload.
...

[SUMMARY:NOTMATCH]
-----

# Instructions
I have given the functional requirements of a software and the code of this software above. 
Carefully judge whether the software has implemented these functions one by one according to the key points of the functional requirements. 
To judge whether the functions are implemented, first, whether the code has tried to implement these functions. Second, if it has tried to implement these functions, whether the code can fully meet the functional requirements in implementation.
The code for implementing the requirements cannot contain pass, cannot be left for future implementation, it must have a complete code implementation


# Action
Follow instruction, generate output and make sure it follows one of the format example.
"""

# Recoding Prompt
RECODING_SYS = """
You are a professional code reviewer engineer; the main goal is to write google-style, elegant, modular, easy to read and maintain code based on the suggestion.
Please regenerate the code based on the matching results of the functional requirements and the code, and make sure to implement all the functions in the functional requirements.
"""

RECODING_THINK = """extract all results that do not meet the requirements:
{result}
"""

RECODNIG = """
Please regenerate the code based on the matching results of the functional requirements and the code, and make sure to implement all the functions in the functional requirements.

# Context

## matching results
{review_suggestion}

## Previous Code
{code}

-----
# Format Example
### main.py
```python
...
```

### ui.py
```python
...
```
-----

# Instruction
1. Use '###' to SPLIT CODE SECTIONS, neither '#' nor '##'. Output format carefully referenced "Format example".
2. Write out EVERY CODE DETAIL, DON'T LEAVE TODO.
3. Only write code result, do not output any other content in the start or in the end.

# Action
Please regenerate the code based on the matching results of the functional requirements and the code, and make sure to implement all the functions in the functional requirements.
Finish after outputting all the code, Do not output any other content.
"""
