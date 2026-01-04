from langchain.tools import tool

@tool
def say_hi() -> str:
    """Hello World tool that prints 'Hi!' """
    return "Hi!"

@tool
def say_hey() -> str:
    """Hello World tool that prints 'Hey!' """
    return "Hey!"


TOOLS = [say_hi, say_hey]