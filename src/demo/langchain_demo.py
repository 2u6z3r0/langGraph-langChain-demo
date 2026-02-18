from langchain_core.prompts import ChatPromptTemplate

from demo.config import content_to_text, get_llm
from demo.markdown_output import render_markdown


def run_langchain_demo(topic: str = "LangChain basics") -> str:
    llm = get_llm(temperature=0.3)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a technical presenter. Keep answers short and demo-friendly.",
            ),
            (
                "human",
                "Give me a 5-bullet explanation of {topic}, then 1 practical example.",
            ),
        ]
    )

    chain = prompt | llm
    response = chain.invoke({"topic": topic})
    return content_to_text(response.content)


if __name__ == "__main__":
    response = run_langchain_demo("How LangChain helps build LLM apps")
    print(render_markdown(f"# LangChain Demo\n\n## Response\n\n{response}"))
