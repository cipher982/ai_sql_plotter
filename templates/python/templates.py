from textwrap import dedent


examples = [
    {
        "query": "The weekly conversion numbers for the past 2 months are 4003, 8678, 9073, 10691, 9807, 9875, 10598, 11457, 7957, and 2239.",
        "answer": dedent(
            """\
            import matplotlib.pyplot as plt

            data = [4003, 8678, 9073, 10691, 9807, 9875, 10598, 11457, 7957, 2239]

            plt.figure(figsize=(7, 3))
            plt.plot(data)

            plt.title('Weekly Conversion Numbers')
            plt.xlabel('Week')
            plt.ylabel('Number of Conversions')

            plt.show()
        """
        ),
    },
    {
        "query": "42118 new users and 28398 return users.",
        "answer": dedent(
            """\
            import matplotlib.pyplot as plt

            new_users = 42118
            return_users = 28398

            plt.figure(figsize=(7, 3))
            plt.bar(['New Users', 'Return Users'], [new_users, return_users])

            plt.title('New vs Return Users')
            plt.ylabel('Number of Users')

            plt.show()
        """
        ),
    },
]


example_template = dedent(
    """\
    User: {query}
    AI: {answer}
    """
)


prefix = dedent(
    """\
    Given a set of input data, plot the data in python. Important notes:
    - This must be valid python code
    - try to use matplotlib for plotting
    - do not use any libraries that are not already installed in the environment
    - keep the code as simple as possible
    - try and use plt.figure(figsize=(7, 3)) to not make the plot too big
"""
)

suffix = dedent(
    """\
    begin!
    User: {query}
    AI: """
)

fix_code_template = """\
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
