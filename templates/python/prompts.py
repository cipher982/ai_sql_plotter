from langchain.prompts import PromptTemplate, FewShotPromptTemplate

from templates.python.templates import prefix, suffix, examples, example_template, fix_code_template


example_python_prompt = PromptTemplate(
    input_variables=["query", "answer"],
    template=example_template,
)


few_shot_python_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_python_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["query"],
    example_separator="\n\n",
)


python_prompt = PromptTemplate(
    input_variables=["query"],
    template=prefix + "\n\n" + suffix,
)


fix_code_prompt = PromptTemplate(
    input_variables=["original_code", "error"],
    template=fix_code_template,
)
