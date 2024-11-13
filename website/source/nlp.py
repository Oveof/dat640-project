from copy import deepcopy
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
from source.tools.show_playlist_content import *
from source.tools.recommend_song_based_on_playlist import recommend_song_based_on_playlist
from source.tools.get_album_info import get_album_info




# examples = [
#     HumanMessage(
#         "what can you do", name="example_user0"
#     ),
#     AIMessage(
#         "I am a helpful playlist assistant, I can help you search for songs.",
#         name="example_assistant0",
#         tool_calls=[],
#     ),
# ]
# examples.extend(search_song_examples)
# examples.extend(add_song_to_playlist_examples)

tool_dict = {
    "search_song": search_song,
    "query_artist_works": get_artist_work,
    "create_playlist": create_playlist,
    "list_playlists": list_playlists,
    "add_song_to_playlist": add_song_to_playlist,
    "remove_song_from_playlist":remove_song_from_playlist,
    "clear_playlists": clear_playlist,
    "delete_playlist": delete_playlist,
    "show_playlist_content": show_playlist_content,

    "recommend_song_based_on_playlist": recommend_song_based_on_playlist,
    "get_album_info": get_album_info,
    }



tools = list(tool_dict.values())

tool_caller_model = ChatOllama(base_url="http://10.10.10.20:11434/", model="mistral", num_ctx=3096, temperature=0.2, system="You one job is to decide if a tool should be called or not. If so call it and dont produce any other output.").bind_tools(tools)
output_formatter_model = ChatOllama(base_url="http://10.10.10.20:11434/", model="mistral-nemo", num_ctx=3096, temperature=0.2, system="You make human readable output, you are part of a larger system, so your job is just to respond to the user with what has happened in the previous stage as if its a part of you. Ensure that you always use data from the database and not pretrained knowledge.")

tool_node = ToolNode(tools)

# Function to call the tool-specialist model
def call_tool_caller_model(state: MessagesState):
    messages = state['messages']
    response = tool_caller_model.invoke(messages)
    return {"messages": [response]}

# Function to decide if the tool node should be executed based on tool calls
def should_continue(state: MessagesState) -> Literal["tools", "output_formatter"]:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "output_formatter"

# Function to call the output formatter model
def call_output_formatter_model(state: MessagesState):
    messages = state['messages']
    # last_tool_output = messages[-1]  # Retrieve the output from the tool-specialist model
    # formatted_prompt = f"Generate a user-friendly summary for this output:\n{last_tool_output.text}"
    response = output_formatter_model.invoke(messages)
    return {"messages": [response]}

# Construct the workflow state graph
workflow = StateGraph(MessagesState)
workflow.add_node("tool_caller", call_tool_caller_model)
workflow.add_node("tools", tool_node)
workflow.add_node("output_formatter", call_output_formatter_model)

workflow.add_edge(START, "tool_caller")  # Start with the tool caller
workflow.add_conditional_edges("tool_caller", should_continue)  # Conditionally go to tools or formatter
workflow.add_edge("tools", "output_formatter")  # Return to tool caller after tools execution

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)


def handle_nonempty_user_input( user_prompt ):
    user = get_current_user()

    final_state = app.invoke(
        {"messages": [
            HumanMessage(content=user_prompt)
        ]},
        config={"configurable": {"thread_id": user.user_session}}
    )

    return final_state["messages"][-1].content


