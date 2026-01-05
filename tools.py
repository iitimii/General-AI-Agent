from langchain.tools import tool

@tool
def say_hi() -> str:
    """Hello World tool that prints 'Hi!' """
    return "Hi!"

@tool
def say_hey() -> str:
    """Hello World tool that prints 'Hey!' """
    return "Hey!"

@tool
def create_file(filename: str, file_content: str) -> str:
    """Tool that creates a file with given filename containing specified content"""

    with open(filename, "w") as f:
        f.write(file_content)

    return f"Created {filename} file"



TOOLS = [say_hi, say_hey, create_file]