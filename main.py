from demo.langchain_demo import run_langchain_demo
from demo.langgraph_demo import run_langgraph_demo


if __name__ == "__main__":
    print("\n=== 1) LangChain ===")
    print(run_langchain_demo("Why LangChain is useful for production demos"))

    print("\n=== 2) LangGraph ===")
    output = run_langgraph_demo("LangGraph for stateful AI workflows")
    print("Plan:\n", output["plan"])
    print("\nDraft:\n", output["draft"])
    print("\nQuality:", output["quality"])
