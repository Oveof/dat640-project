from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

@tool
def get_artist_work(artist: Annotated[str, "name of artist"])-> Annotated[dict, "A dict of all works by the artist"]:
    """Provides a dict with works by artist"""

    return 