from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.agents.browser_agent import run_browser_agent
from app.agents.ux_analyst import run_ux_analyst
from app.agents.accessibility_agent import run_accessibility_agent
from app.agents.report_agent import run_report_agent

class AuditState(TypedDict):
    url: str
    browser_result: dict
    ux_result: dict
    accessibility_result: dict
    final_report: dict
    error: str

async def browser_node(state: AuditState) -> AuditState:
    result = await run_browser_agent(state["url"])
    return {**state, "browser_result": result}

async def ux_node(state: AuditState) -> AuditState:
    result = await run_ux_analyst(
        state["browser_result"]["screenshots"],
        state["url"]
    )
    return {**state, "ux_result": result}

async def accessibility_node(state: AuditState) -> AuditState:
    result = run_accessibility_agent(
        state["browser_result"]["html"],
        state["url"]
    )
    return {**state, "accessibility_result": result}

async def report_node(state: AuditState) -> AuditState:
    result = run_report_agent(
        state["url"],
        state["ux_result"],
        state["accessibility_result"]
    )
    return {**state, "final_report": result}

def build_pipeline():
    graph = StateGraph(AuditState)
    graph.add_node("browser", browser_node)
    graph.add_node("ux_analyst", ux_node)
    graph.add_node("accessibility", accessibility_node)
    graph.add_node("report", report_node)
    graph.set_entry_point("browser")
    graph.add_edge("browser", "ux_analyst")
    graph.add_edge("ux_analyst", "accessibility")
    graph.add_edge("accessibility", "report")
    graph.add_edge("report", END)
    return graph.compile()

async def run_audit_pipeline(url: str) -> dict:
    pipeline = build_pipeline()
    initial_state = AuditState(
        url=url,
        browser_result={},
        ux_result={},
        accessibility_result={},
        final_report={},
        error=""
    )
    final_state = await pipeline.ainvoke(initial_state)
    return final_state["final_report"]
