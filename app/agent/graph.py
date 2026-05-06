from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END, add_messages
from langchain.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from typing import TypedDict, Optional, Any, Literal, Annotated
from app.agent.tools import tools_list

from langgraph.prebuilt import ToolNode, tools_condition
from app.core.config import settings


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


llm = init_chat_model(
    "gpt-4o-mini", model_provider="openai", api_key=settings.OPENAI_API_KEY
)

llm_with_tools = llm.bind_tools(tools=tools_list)


# --------------------
# NODES
# --------------------
async def react_node(state: AgentState) -> AgentState:
    messages = state["messages"]

    system_message = SystemMessage(content=f"""
You are a helpful assistant that can use tools to answer questions. You will be given a question and a list of tools you can use to answer the question. You can use the tools as many times as you want,If you need to use a tool, you should call it with the appropriate input arguments. If you don't need to use a tool, you can just answer the question directly.
""")

    response = await llm_with_tools.ainvoke([system_message] + messages)

    return {"messages": [response]}


tool_node = ToolNode(tools=tools_list)


# --------------------
# GRAPH
# --------------------
graph = StateGraph(state_schema=AgentState)
graph.add_node("react_node", react_node)
graph.add_node("tool_node", tool_node)


graph.add_edge(START, "react_node")
graph.add_conditional_edges(
    "react_node",
    tools_condition,
    {"tools": "tool_node", "__end__": END},
)

graph.add_edge("tool_node", "react_node")


workflow = graph.compile()
