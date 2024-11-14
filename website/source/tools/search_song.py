import json
from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Song, get_current_user, session_maker

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload


@tool
def search_or_suggest_song(song_title:
    Annotated[str, "something to search with"]
    ) -> Annotated[List[dict], "list of songs formatted in json with attributes"]:
    """Search or suggest a song in the database"""


    print("searched for song")
    session = session_maker()
    search_pattern = f"%{song_title.lower()}%"
    stmt = (
        select(Song)
        .options(
            selectinload(Song.artists),
            selectinload(Song.albums),
            selectinload(Song.genres),
        )
        .where(func.lower(Song.name).like(search_pattern))
    )

    results = session.execute(stmt).scalars().all()
    songs_list = [song.to_dict() for song in results]
    if len(songs_list) > 5:
        songs_list = songs_list[:5]

    print(songs_list)
    return json.dumps(songs_list, indent=4)

