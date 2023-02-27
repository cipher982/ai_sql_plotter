from textwrap import dedent

from langchain.prompts import PromptTemplate, FewShotPromptTemplate


EXAMPLES = [
    {
        "query": "The weekly conversion numbers for the past 2 months are 4003, 8678, 9073, 10691, 9807, 9875, 10598, 11457, 7957, and 2239.",
        "answer": dedent("""\
            import matplotlib.pyplot as plt

            data = [4003, 8678, 9073, 10691, 9807, 9875, 10598, 11457, 7957, 2239]

            plt.figure(figsize=(7, 3))
            plt.plot(data)

            plt.title('Weekly Conversion Numbers')
            plt.xlabel('Week')
            plt.ylabel('Number of Conversions')

            plt.show()
        """)
    },
    {
        "query": "42118 new users and 28398 return users.",
        "answer": dedent("""\
            import matplotlib.pyplot as plt

            new_users = 42118
            return_users = 28398

            plt.figure(figsize=(7, 3))
            plt.bar(['New Users', 'Return Users'], [new_users, return_users])

            plt.title('New vs Return Users')
            plt.ylabel('Number of Users')

            plt.show()
        """)
    }
]


EXAMPLE_TEMPLATE = dedent("""\
    User: {query}
    AI: {answer}
    """)

EXAMPLE_PROMPT = PromptTemplate(
    input_variables=["query", "answer"],
    template=EXAMPLE_TEMPLATE,
)

PREFIX = dedent("""\
    Given a set of input data, plot the data in python. Important notes:
    - This must be valid python code
    - try to use matplotlib for plotting
    - do not use any libraries that are not already installed in the environment
    - keep the code as simple as possible
    - try and use plt.figure(figsize=(7, 3)) to not make the plot too big
""")

SUFFIX = dedent("""\
    begin!
    User: {query}
    AI: """)


few_shot_python_template = FewShotPromptTemplate(
    examples=EXAMPLES,
    example_prompt=EXAMPLE_PROMPT,
    prefix=PREFIX,
    suffix=SUFFIX,
    input_variables=["query"],
    example_separator="\n\n",
)
