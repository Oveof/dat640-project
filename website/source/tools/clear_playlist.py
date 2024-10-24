from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

@tool
def clear_playlist(playlist_id: Annotated[int, "id of the playlist"])-> Annotated[bool, "True or False, means success or failure to remove all songs from playlist"]:
    """Delete all songs from playlist"""

    return 