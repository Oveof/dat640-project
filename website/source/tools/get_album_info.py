

from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Album, Song, get_current_user, session_maker, song_album
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


@tool
def get_album_info(
    album_id: Annotated[int, "album_id"]
) -> Annotated[dict, "Dictionary with album info"]:
    """This functions gets info for a specific album"""

    print(f"CALLED GET ALBUM INFO: ALBUM NAME {album_id}")
    user = get_current_user()

    try:
        return db_get_album_info(album_id)
    except Exception as exception:
        print(exception)
        return "Function call failed"


def db_get_album_info(album_id):
    session = session_maker()

    # Fetch the user's playlist
    stmt = select(Album).filter_by(id=album_id)
    album = session.execute(stmt).scalars().first()
    if album is None:
        return {}
    songs = session.query(Song).join(song_album).filter(song_album.c.album_id == album.id).all()
    songs = [{"name": song.name} for song in songs]
    
    album_info = {"id": album.id, "name": album.name, "songs": songs, "release_year": album.release_year} 
    print(album_info)
    return album_info

