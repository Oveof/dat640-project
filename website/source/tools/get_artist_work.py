import json
from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Artist, Song, song_artists, session_maker

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload

@tool
def get_artist_work(artist_name: Annotated[str, "name of artist"])-> Annotated[dict, "A dict of all works by the artist"]:
    """Provides a dict with works by artist"""
    try:
        return db_get_artist_work(artist_name)
    except Exception as exception:
        print(exception)
        return "Function call failed"

def db_get_artist_work(artist_name: str) -> dict:
    session = session_maker()
    search_pattern = f"%{artist_name.lower()}%"

    artist_stmt = (
        select(Artist)
        .where(func.lower(Artist.name).like(search_pattern))
        .limit(1)
    )

    artist = session.execute(artist_stmt).scalars().first()

    if not artist:
        return {}

    song_stmt = (
        select(Song)
        .options(selectinload(Song.albums))
        .join(song_artists)
        .where(song_artists.c.artist_id == artist.id)
    )

    songs = session.execute(song_stmt).scalars().all()

    artist_data = {
        "artist": artist.name,
        "songs": [
            {
                "song_name": song.name,
                "albums": [{"album_name": album.name, "release_date": album.release_date} for album in song.albums]
            }
            for song in songs
        ]
    }
    return artist_data
