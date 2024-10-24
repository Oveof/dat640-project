from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage



@tool
def remove_song_from_playlist(
    song_id: Annotated[int, "song id"],
    playlist_id: Annotated[int, "playlist id"]
    ) -> Annotated[bool, "True or False, means success or failure to remove song."]:
    """Remove a song from a playlist"""

    return True