from typing import Annotated, Literal, Sequence, TypedDict
import ollama

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import render_text_description
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.graph.message import add_messages

from langchain_core.messages import BaseMessage


from source.tools.add_song import add_song_to_playlist, add_song_to_playlist_examples
from source.tools.search_song import search_song, search_song_examples
from source.tools.list_user_playlist import list_user_playlists

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from source.tools.list_artist_work import get_artist_work


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
    "add_song_to_playlist": add_song_to_playlist,
    "list_user_playlist": list_user_playlists,
    "search_song": search_song,
    "query_artist_works": get_artist_work
    }

tools = list(tool_dict.values())

ollama_model = ChatOllama(base_url="http://10.10.10.20:11434/",model="mistral-small").bind_tools(tools) # ollama.Client(host='10.10.10.20:11434'))


system_prompt = f"""
You are a helpful chat assistant which manages playlists.

Strict rules:
    1. Do not call tools unless its really obvious that its what the user wants.
    2. Interact with the user.
    3. Do not talk about anything other than music related things.
# """
# class State(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], add_messages]
#     language: str

# workflow = StateGraph(state_schema=MessagesState)
# ollama_model.bind(tools=tools)

# few_shot_prompt = ChatPromptTemplate.from_messages(
# [
#     ("system", system_prompt),
#     *examples,
# ])

# chain = {"query": RunnablePassthrough()} | few_shot_prompt | ollama_model


# def call_model(state: State):
#     response = chain.invoke(state["messages"])
#     return {"messages": response}


# workflow.add_edge(START, "model")
# workflow.add_node("model", call_model)

# memory = MemorySaver()
# app = workflow.compile(checkpointer=memory)


# config = {"configurable": {"thread_id": "abc123"}}

# def handle_nonempty_user_input( user_prompt ):

#     input_dict = {
#         "messages": [HumanMessage(user_prompt)],
#     }
#     output = app.invoke(input_dict, config)

#     content = ""
#     tool_calls = []


#     while content=="":
#         content = output["messages"][-1].content
#         print(content)
#         # tool_call_message=  """You are in a tool calling loop you have the following options:
#         #     - Call another tool if you are not finished if so do not write any text, just call the appropriate tool.
#         #     - The desired operation is finished, if so respond to the user don't call any more tools.
#         # """
#         for tool_call in tool_calls:
#             selected_tool = tool_dict[tool_call["name"].lower()]
#             tool_output = selected_tool.invoke(tool_call["args"])

#             print(tool_output)


#     return content
tool_node = ToolNode(tools)

def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END

def call_model(state: MessagesState):
    messages = state['messages']
    response = ollama_model.invoke(messages)
    # We return a list, because this will get added to the existing list
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
    final_state = app.invoke(
        {"messages": [HumanMessage(content=user_prompt)]},
        config={"configurable": {"thread_id": 101}}
    )

    return final_state["messages"][-1].content
