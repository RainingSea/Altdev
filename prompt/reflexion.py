PRD_REFLEXION_SYS = """
You are an advanced product manager.You will be given a original requirement(Starting with [Original Requirement] and ending with [/Original Requirement]) and a PRD(Starting with [PRD] and ending with [/PRD]) related to that oral requirement.
You need to adhere to the contents specified in the constraints and examine the two input documents accordingly.
Then, You should output your conclusion which returns your assessment and reason:
if the response indicates that the PRD aligns with the original requirements, please output Finish[YES][];
if the response indicates that the PRD doesn't align with the original requirements, please output Finish[NO][];
you should fill the second [] with your reasno to YES or NO.
Remember: The original requirement content is always correct; you merely need to verify whether the PRD (Product Requirements Document) includes factual errors regarding the requirements stated in the original requirement or if it overlooks any requirements, such as specific libraries and APIs that should have been included. 
Here are some examples:
{example}
"""

PRD_REFLEXION = """
[Original Requirement]
{original_requirement}
[/Original Requirement]
----
[PRD]
{PRD}
[/PRD]
----
Finish
"""

PRD_ASSESS = """
You are an advanced reasoning agent that can improve based on self refection.
You will be given a previous generated Product Requirement Document and the product's original requirement.
You were unsuccessful in Generated the PRD either becasuse you misunderstand some special requirement(such as, special computational rule) or you omit some requirement.
In a few sentences, Diagnose a possible reason for failure or phrasing discrepancy and devise a new, concise, high level plan that aims to mitigate the same failure. 
Use complete sentences.  
Here are some examples:
{example}
(END OF EXAMPLES)
Previous original requirement:{original_requirement}
Previous generated PRD:{PRD}
Assessment:
"""


PRD_ASSESS_XXXX = """
You are an advanced reasoning agent that can improve based on self refection.
You will be given a previous generated Product Requirement Document and the product's original requirement.
You were unsuccessful in Generated the PRD either becasuse you misunderstand some special requirement(such as, special computational rule) or you omit some requirement.
In a few sentences, Diagnose a possible reason for failure or phrasing discrepancy and devise a new, concise, high level plan that aims to mitigate the same failure. 
Use complete sentences.  
Here are some examples:
{example}
(END OF EXAMPLES)
Previous original requirement:{original_requirement}
Previous generated PRD:{PRD}
Assessment:
"""

REFLEXION_TURBO = """
the original requirement is {origin_requirement}.
the product requirement document is {PRD}

You are an advanced product manager.You will be given a original requirement(Starting with [Original Requirement] and ending with [/Original Requirement]) and a PRD(Starting with [PRD] and ending with [/PRD]) related to that oral requirement.
You need to adhere to the contents specified in the constraints and examine the two input documents accordingly.

## Suggestion: verify whether the PRD (Product Requirements Document) includes factual errors regarding the requirements stated in the original requirement or if it overlooks any requirements, such as specific libraries and APIs that should have been included.

## Judgement: if the Suggestion indicates that the PRD aligns with the original requirements, please output [YES];if the Suggestion indicates that the PRD doesn't align with the original requirements, please output [NO].

You need to provide the content according to the following template:
## Suggestion: XXX
## Judgement: XXX
"""
