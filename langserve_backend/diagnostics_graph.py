from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from tools.symptom_checker import check_symptom
from tools.diagnosis_tool import ai_diagnos
from typing import TypedDict


class DiagnosisState(TypedDict):
    input: str
    symptom_area: str
    diagnosis: str


def build_diagnostics_graph() :
    """Builds the diagnostics graph for handling medical diagnostics."""
    
    graph = StateGraph(DiagnosisState)

    def symptom_step(state: DiagnosisState) -> DiagnosisState:
        """A step to collect user input for the symptom area."""
        return {
            "input": state["input"], 
            "symptom_area": check_symptom.invoke(state["symptom_area"]),
            "diagnosis": state.get("diagnosis", "")}

    graph.add_node(
        "symptom_check",
        RunnableLambda(symptom_step),
    )


    def diagnosis_step(state: DiagnosisState) -> DiagnosisState:
        """A step to perform diagnosis based on the symptom area."""
        return {
            "input": state["input"],
            "symptom_area": state["symptom_area"],
            "diagnosis": ai_diagnos.invoke(state["input"]),
        }
    
    graph.add_node(
        "diagnosis_step", 
        RunnableLambda(diagnosis_step)
    )


    graph.set_entry_point("symptom_check")
    graph.add_edge("symptom_check", "diagnosis_step")
    graph.add_edge("diagnosis_step", END)

    return graph.compile()