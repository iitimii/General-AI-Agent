from langchain.messages import HumanMessage
from agent import agent





def main():
    messages = [HumanMessage(content="Say hi to me 3 times, then hey twice")]
    messages = agent.invoke({"messages": messages})

    for m in messages["messages"]:
        m.pretty_print()
    

if __name__ == "__main__":
    main()