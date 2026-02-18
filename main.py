from demo.langchain_demo import run_langchain_demo
from demo.langgraph_demo import run_langgraph_demo
from demo.markdown_output import render_markdown

if __name__ == "__main__":
    print("\n=== 1) LangChain ===")
    langChainOutput = run_langchain_demo("Why LangChain is useful for production demos")
    print(render_markdown(langChainOutput))
    print("\n=== 2) LangGraph ===")
    output = run_langgraph_demo("LangGraph for stateful AI workflows")
    print("Plan:\n", render_markdown(output["plan"]))
    print("\nDraft:\n", render_markdown(output["draft"]))
    print("\nQuality:", render_markdown(output["quality"]))
