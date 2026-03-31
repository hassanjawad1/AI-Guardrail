from typing import TypedDict

class GuardrailState(TypedDict):
    user_input: str

    # Pre-checks
    risk_level: str
    toxicity_score: float
    pii_detected: bool

    # LLM
    llm_output: str

    # Post-check
    safe: bool

    # Final
    final_output: str