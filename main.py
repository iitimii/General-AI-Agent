from langchain.messages import HumanMessage
from IPython.display import Image, display
from agent import agent, MessagesState





def main():
    # display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

    config = {"configurable": {"thread_id": "1"}}
    state = MessagesState(messages=[HumanMessage(content="Say hi to me 3 times, then hey twice")],
                          llm_calls=0)
    
    messages = agent.invoke(state, config=config)

    for m in messages["messages"]:
        m.pretty_print()
    

if __name__ == "__main__":
    main()