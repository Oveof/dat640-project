from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Album, Song, get_current_user, session_maker, song_album
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


@tool
def search_album(
    album_name: Annotated[str, "album_name"]
) -> Annotated[dict, "List of albums"]:
    """This functions gets all albums matching name"""

    user = get_current_user()

    try:
        return db_search_album(album_name)
    except Exception as exception:
        print(exception)
        return "Function call failed"


def db_search_album(album_name):
    session = session_maker()

    # Fetch the user's playlist
    search_pattern = f"%{album_name.lower()}%"
    stmt = (
        select(Album)
        .where(func.lower(Album.name).like(search_pattern))
    )

    albums = session.execute(stmt).scalars().all()
    if albums is None:
        return []
    
    albums = [{"id": album.id, "name": album.name} for album in albums ]
    return albums

