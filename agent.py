import operator
from typing import Literal
from typing_extensions import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langchain.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import InMemorySaver

from llm import model
from tools import TOOLS

tools_by_name = {tool.name: tool for tool in TOOLS}
model_with_tools = model.bind_tools(TOOLS)


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


# Node
def llm_call(state: MessagesState):
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

#could also be
# def llm_call(state: MessagesState) -> Command[Literal["tool_node", END]]:
#     state = {
#         "messages": [
#             model_with_tools.invoke(
#                 [
#                     SystemMessage(
#                         content="You are a helpful assistant tasked with performing actions required"
#                     )
#                 ] + state["messages"]
#             )
#         ],
#         "llm_calls": state.get("llm_calls", 0) + 1
#     }

#     next_node = "tool_node" if state["messages"][-1].tool_calls else END

#     return Command(update=state, goto=next_node)


def tool_node(state: MessagesState):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

# conditional Edge
def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tool_node"

    return END


agent_builder = StateGraph(MessagesState)
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)


agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")

memory = InMemorySaver()
agent = agent_builder.compile(checkpointer=memory)