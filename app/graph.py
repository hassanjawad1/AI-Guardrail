from langgraph.graph import StateGraph, END
from app.state import GuardrailState
from app.nodes import (
    detect_pii,
    input_safety,
    decision,
    generate,
    output_check,
    rewrite,
    block,
    finalize,
)

builder = StateGraph(GuardrailState)

builder.add_node("pii", detect_pii)
builder.add_node("safety", input_safety)
builder.add_node("decision", decision)
builder.add_node("generate", generate)
builder.add_node("output_check", output_check)
builder.add_node("rewrite", rewrite)
builder.add_node("block", block)
builder.add_node("finalize", finalize)

builder.set_entry_point("pii")

builder.add_edge("pii", "safety")
builder.add_edge("safety", "decision")

builder.add_conditional_edges(
    "decision",
    lambda state: state["action"],   # ✅ read from state
    {
        "block": "block",
        "rewrite": "rewrite",
        "allow": "generate",
    },
)

builder.add_edge("generate", "output_check")

builder.add_conditional_edges(
    "output_check",
    lambda state: "rewrite" if not state["safe"] else "finalize",
    {
        "rewrite": "rewrite",
        "finalize": "finalize",
    },
)

builder.add_edge("rewrite", "finalize")
builder.add_edge("block", END)
builder.add_edge("finalize", END)

graph = builder.compile()