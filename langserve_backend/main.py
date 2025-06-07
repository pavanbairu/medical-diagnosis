from fastapi import FastAPI
from langserve import add_routes
from diagnostics_graph import build_diagnostics_graph
import uvicorn

app = FastAPI()

graph = build_diagnostics_graph()

add_routes(
    app,
    graph,
    path="/diagnosis",
)

if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000)