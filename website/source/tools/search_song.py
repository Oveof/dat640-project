import json
from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Song, session_maker

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload


@tool
def search_song(song_title:
    Annotated[str, "something to search with"]
    ) -> Annotated[List[dict], "list of songs formatted in json with attributes"]:
    """Search for a song in the database"""
    session = session_maker()
    search_pattern = f"%{song_title.lower()}%"
    stmt = (
        select(Song)
        .options(
            selectinload(Song.artists),
            selectinload(Song.albums)
        )
        .where(func.lower(Song.name).like(search_pattern))
    )

    results = session.execute(stmt).scalars().all()
    songs_list = [song.to_dict() for song in results]
    if len(songs_list) > 5:
        songs_list = songs_list[:5]

    return json.dumps(songs_list, indent=4)


search_song_examples = [
    HumanMessage(
        "search for happy", name="example_user"
    ),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            { "name": "search_song", "args": {"song_title": "happy"},"id": "1" }
        ],
    ),
    ToolMessage("""{ id: 231, name:  happy, Artist: Pharrell Williams, Release: 21.11.2023, Genre: [Soul, R&B] }""", tool_call_id="1"),
    AIMessage(
        """I found the following result when searching for happy.
        Song: Happy
        Artist: Pharell Williams
        Release date: 21.11.2023
        Genre: Soul, R&B
        """,
        name="example_assistant",
    ),
    
    HumanMessage(
        "search for what in this world", name="example_user2"
    ),
    AIMessage(
        "",
        name="example_assistant2",
        tool_calls=[
            { "name": "search_song", "args": {"song_title": "what in this world"},"id": "2" }
        ],
    ),
    ToolMessage("""{ }""", tool_call_id="3"),

    AIMessage(
        """I was unable to find anything matching 'what in the world'.""",
        name="example_assistant2",
    ),

]
