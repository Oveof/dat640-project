from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage



@tool
def list_user_playlists()-> Annotated[str,"a dict of the users playlists"]:
    """List of users playlist"""
    return "{ 0: Something Good, 1: Life is good, 3: We love the world, 4: Nice and quiet }"

