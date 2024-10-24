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

    session = session_maker()
    search_pattern = f"%{artist_name.lower()}%"

    # Query the first artist with a case-insensitive partial match on the name
    artist_stmt = (
        select(Artist)
        .where(func.lower(Artist.name).like(search_pattern))
        .limit(1)
    )

    artist_name = session.execute(artist_stmt).scalars().first()  # Get the first matching artist

    if artist_name:
        # Now, query for the songs and albums associated with this artist
        song_stmt = (
            select(Song)
            .options(selectinload(Song.albums))  # Load albums for each song
            .join(song_artists)  # Join the association table song_artists
            .where(song_artists.c.artist_id == artist_name.id)  # Filter by artist ID
        )

        songs = session.execute(song_stmt).scalars().all()  # Fetch all matching songs

        # Serialize the artist's works (songs and albums) to JSON-compatible format
        artist_data = {
            "artist": artist_name.name,
            "songs": [
                {
                    "song_name": song.name,
                    "albums": [{"album_name": album.name, "release_date": album.release_date} for album in song.albums]
                }
                for song in songs
            ]
        }
        return artist_data
    else:
        return {"error": "Artist not found"}
