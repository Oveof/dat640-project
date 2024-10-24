from typing import Annotated, Literal, Sequence, TypedDict
import ollama

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import render_text_description
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage

from source.db import get_current_user


from source.tools.list_playlists import *
from source.tools.create_playlist import *
from source.tools.clear_playlist import *
from source.tools.delete_playlist import *
from source.tools.add_song_to_playlist import *
from source.tools.remove_song_from_playlist import *
from source.tools.search_song import *
from source.tools.get_artist_work import *
from source.tools.get_song_genre import *




examples = [
    HumanMessage(
        "what can you do", name="example_user0"
    ),
    AIMessage(
        "I am a helpful playlist assistant, I can help you search for songs.",
        name="example_assistant0",
        tool_calls=[],
    ),
]
examples.extend(search_song_examples)
examples.extend(add_song_to_playlist_examples)

tool_dict = {
    "search_song": search_song,
    "query_artist_works": get_artist_work,
    "query_song_genre": get_song_genre,

    "create_playlist": create_playlist,
    "list_playlists": list_playlists,
    "add_song_to_playlist": add_song_to_playlist,
    "remove_song_from_playlist":remove_song_from_playlist,
    "clear_playlists": clear_playlist,
    "delete_playlist": delete_playlist,
    
    
    }

tools = list(tool_dict.values())

ollama_model = ChatOllama(base_url="http://10.10.10.20:11434/",model="mistral-small").bind_tools(tools) # ollama.Client(host='10.10.10.20:11434'))


system_prompt = f"""
You are a helpful chat assistant which manages playlists.

Strict rules:
    1. Use the tools at your disposal.
    2. Interact with the user.
    3. Do not talk about anything other than music related things.
# """

tool_node = ToolNode(tools)

def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

def call_model(state: MessagesState):
    messages = state['messages']
    if not any(type(message) == SystemMessage for message in messages):
        system_message = SystemMessage(content=system_prompt)
        messages.insert(0, system_message)  # Insert at the beginning to avoid altering the flow

    response = ollama_model.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent",should_continue)
workflow.add_edge("tools","agent")
# workflow.add_conditional_edges("agent",should_continue)
# workflow.add_conditional_edges("tools","tool")

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)


def handle_nonempty_user_input( user_prompt ):
    user = get_current_user()
    final_state = app.invoke(
        {"messages": [HumanMessage(content=user_prompt)]},
        config={"configurable": {"thread_id": user.user_session}}
    )

    return final_state["messages"][-1].content
