from langchain.tools import tool

@tool
def say_hi() -> None:
    """Hello World tool that prints 'Hi!' """
    print("Hi!")


TOOLS = []