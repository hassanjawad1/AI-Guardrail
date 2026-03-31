from app.lib import FastAPI, BaseModel
from app.graph import graph

app = FastAPI()


class Query(BaseModel):
    text: str


@app.post("/chat")
def chat(query: Query):
    result = graph.invoke({
        "user_input": query.text
    })

    return {
        "input": query.text,
        "output": result["final_output"]
    }