from app.models import call_llm, safety_check_llm
from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()


# 🔐 PII Detection
def detect_pii(state):
    results = analyzer.analyze(text=state["user_input"], language="en")
    return {"pii_detected": len(results) > 0}


# 🧠 Input Safety Check
def input_safety(state):
    result = safety_check_llm(state["user_input"])
    return {
        "toxicity_score": result["toxicity_score"],
        "risk_level": result["risk_level"]
    }


# ⚖️ Decision Node
def decision(state):
    if state["pii_detected"]:
        action = "block"
    elif state["toxicity_score"] > 0.8:
        action = "block"
    elif state["risk_level"] == "high":
        action = "rewrite"
    else:
        action = "allow"

    return {"action": action}   # ✅ MUST return dict


# 🤖 LLM Generation
def generate(state):
    response = call_llm(state["user_input"])
    return {"llm_output": response}


# 🧠 Output Safety Check
def output_check(state):
    result = safety_check_llm(state["llm_output"])
    return {"safe": result["safe"]}


# ✍️ Rewrite unsafe output
def rewrite(state):
    prompt = f"""
    Rewrite safely and professionally:

    {state.get("llm_output", state["user_input"])}
    """
    safe_output = call_llm(prompt)
    return {"final_output": safe_output}


# 🚫 Block response
def block(state):
    return {
        "final_output": "❌ Request blocked due to safety concerns."
    }


# ✅ Final pass
def finalize(state):
    return {
        "final_output": state.get("final_output", state["llm_output"])
    }