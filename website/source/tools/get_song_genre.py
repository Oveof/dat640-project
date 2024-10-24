import json
from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Artist, Song, song_artists, session_maker

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload

@tool
def get_song_genre(song_name: Annotated[str, "name of song"])-> Annotated[List, "A list of genres for song"]:
    """Provides list of genres for song"""
    try:
        return db_get_song_genre(song_name)
    except Exception as exception:
        print(exception)
        return "Function call failed"

def db_get_song_genre(song_name: str) -> List:
    session = session_maker()
    search_pattern = f"%{song_name.lower()}%"
    song = session.query(Song).filter_by(name=song_name).first()
    if song is None:
        return []
    genres = song.genres
    genre_details = [{"id": genre.id, "name": genre.name} for genre in genres]
    return genre_details
