from typing import TypedDict, cast

from langgraph.graph import END, START, StateGraph

from demo.config import content_to_text, get_llm


class DemoState(TypedDict):
    topic: str
    plan: str
    draft: str
    quality: str


def create_graph():
    llm = get_llm(temperature=0.2)

    def planner(state: DemoState) -> DemoState:
        prompt = (
            "Create a 3-step plan for a short technical demo talk about: "
            f"{state['topic']}. Return plain text."
        )
        plan = content_to_text(llm.invoke(prompt).content)
        return {**state, "plan": plan}

    def writer(state: DemoState) -> DemoState:
        prompt = (
            "Write a short demo script (120-180 words) using this plan:\n"
            f"{state['plan']}"
        )
        draft = content_to_text(llm.invoke(prompt).content)
        return {**state, "draft": draft}

    def reviewer(state: DemoState) -> DemoState:
        prompt = (
            "Review this draft and output ONLY one word: PASS or FAIL.\n"
            "Use PASS if it is clear, concise, and practical.\n\n"
            f"Draft:\n{state['draft']}"
        )
        quality = content_to_text(llm.invoke(prompt).content).strip().upper()
        if "PASS" not in quality:
            quality = "FAIL"
        else:
            quality = "PASS"
        return {**state, "quality": quality}

    def revise(state: DemoState) -> DemoState:
        prompt = (
            "Revise this draft to make it clearer and more practical. Keep it under 180 words.\n\n"
            f"{state['draft']}"
        )
        draft = content_to_text(llm.invoke(prompt).content)
        return {**state, "draft": draft, "quality": "PASS"}

    def route_after_review(state: DemoState) -> str:
        if state["quality"] == "PASS":
            return "end"
        return "revise"

    graph = StateGraph(DemoState)
    graph.add_node("planner", planner)
    graph.add_node("writer", writer)
    graph.add_node("reviewer", reviewer)
    graph.add_node("revise", revise)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "writer")
    graph.add_edge("writer", "reviewer")
    graph.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "revise": "revise",
            "end": END,
        },
    )
    graph.add_edge("revise", END)

    return graph.compile()


def run_langgraph_demo(topic: str = "LangGraph for agent workflows") -> DemoState:
    app = create_graph()
    initial_state: DemoState = {
        "topic": topic,
        "plan": "",
        "draft": "",
        "quality": "",
    }
    return cast(DemoState, app.invoke(initial_state))


if __name__ == "__main__":
    print("=== LangGraph Demo ===")
    result = run_langgraph_demo("How to build robust LLM workflows")
    print("Plan:\n", result["plan"])
    print("\nFinal Draft:\n", result["draft"])
    print("\nQuality:", result["quality"])
