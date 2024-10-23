from langchain_core.tools import tool
from typing import Annotated, List




@tool
def search_song(song_title: 
    Annotated[str, "something to search with"]
    ) -> Annotated[List[dict], "list of songs formatted in json with attributes"]:
    """Search for a song in the database"""

    return []





tools = [search_song]
