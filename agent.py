from llm import model
from tools import TOOLS

from langchain.messages import AnyMessage, SystemMessage, HumanMessage
from typing_extensions import TypedDict, Annotated
import operator

tools_by_name = {tool.name: tool for tool in TOOLS}
model_with_tools = model.bind_tools(TOOLS)


class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


# Node
def llm_call(state: dict):
    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing actions required"
                    )
                ] + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


def tool_node(state: dict):
    result = []