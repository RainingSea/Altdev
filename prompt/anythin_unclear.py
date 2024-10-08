CHECK_UNCLEAR = """
<task>
{task}
</task>
<PRD>
{requirement documents}
</PRD>

You are an architect in a software company with four members (project manager, architect, project manager and engineer).You receive a requirements document from your product manager (starting with <prd> and ending with </prd>).Before carrying out the architecture design, you need to review this requirement document.Please note that this development is only aimed at developing a demo that can realize the functions in the original requirements(starting from <task> and ending with </task>).

Requirement: Fill in the following missing information,note that all sections are response with code form separately.
Max Output: 8192 chars or 2048 tokens. Try to use them up.

Attention: Use '##' to split sections, not '#', and '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote.
##Need Requirements Clarification：Provide as Plain text.List the unclear contents in the requirements document that you believe need clarification.

You need to provide the content according to the following template:
##Requirements Clarification：XX
"""

RESPONSE_UNCLEAR = """
<task>
{task}
</task>
<PRD>
{requirement document}
</PRD>

<Anything Unclear>
{Anything Unclear}
</Anything Unclear>

You are a product manager in a software company with four members (product manager, architect, project manager and engineer).The architect thinks that the content of the requirement document you wrote (starting from <prd> and ending with </prd>) is not clear enough, and provides you with some questions that need to be answered (starting from <Anything Unclear> and ending with <Anything Unclear>).

Requirement: Fill in the following missing information based on the requirements document, note that all sections are response with code form separately
Max Output: 8192 chars or 2048 tokens. Try to use them up.

Attention: Use '##' to split sections, not '#', and '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote.

##Requirements Clarification：Provide as Plain text.Based on the original requirements(starting from <task> and ending with </task>),list the answers to the questions (starting from <Anything Unclear> and ending with <Anything Unclear>).

You need to provide the content according to the following template:
##Requirements Clarification：XX
"""
