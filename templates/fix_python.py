from langchain.prompts.prompt import PromptTemplate


fix_code_template = """
You have been given a block of Python code that is supposed to perform a certain task, but it might have a bug in it. 
Your task is to analyze the code and identify any bugs or errors that may be preventing it from working correctly.
Keep in mind the code may have multiple bugs, or may not have any bugs at all. If you think the code is correct,
you can leave it as is. If you think the code is incorrect, you can fix it.
Use the following format:

Original Code: "original code here"
Error: "error here"
Fixed Code: "final fixed code here"

Begin!

Original Code: {original_code}
Error: {error}
Fixed Code: """

fix_code_prompt = PromptTemplate(
    input_variables=["original_code", "error"],
    template=fix_code_template,
)