from langchain.messages import HumanMessage
from langgraph.types import Command
from IPython.display import Image, display
from agent import agent, MessagesState





def main():
    # display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

    # init_message = "Say hi to me 3 times, then hey twice"
    init_message = "create a txt file with name hobbies containing a list of common hobbies number 1-10"

    state = MessagesState(messages=[HumanMessage(content=init_message)],
                          llm_calls=0)
    config = {"configurable": {"thread_id": "1"}}
    messages = agent.invoke(state, config=config)
    if "__interrupt__" in messages:
        interrupt_msg = messages["__interrupt__"][-1].value
        human_response = input(f"{interrupt_msg['message']}: ")

        messages = agent.invoke(Command(resume={"action": human_response}), config=config)

    for m in messages["messages"]:
        m.pretty_print()
    

if __name__ == "__main__":
    main()