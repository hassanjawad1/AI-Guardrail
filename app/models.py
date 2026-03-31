from app.lib import Groq, os, json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# Safety via LLM
def safety_check_llm(text: str):
    prompt = f"""
    Analyze this text:
    "{text}"

    Return JSON:
    {{
        "toxicity_score": 0-1,
        "risk_level": "low | medium | high",
        "safe": true/false
    }}
    """

    response = call_llm(prompt)

    # naive parsing

    try:
        return json.loads(response)
    except:
        return {"toxicity_score": 0.5, "risk_level": "medium", "safe": True}