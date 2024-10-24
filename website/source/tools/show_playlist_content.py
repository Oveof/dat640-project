from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Playlist, Song, get_current_user, session_maker, playlist_song
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


@tool
def show_playlist_content(playlist_id: Annotated[int, "playlist id"]) -> Annotated[List[Annotated[dict, "Song details"]], "List of the songs in the playlist"]:
    """List the contents of a playlist"""

    print(f"LIST PLAYLIST CONTENT WAS CALLED {playlist_id}")
    user = get_current_user()
    try:
        result= db_get_playlist_songs(playlist_id,user.id)
        print(result)
        return result
    except Exception as exception:
        print(exception)
        return "Function call failed"


def db_get_playlist_songs(playlist_id: int,user_id:int):
    session = session_maker()

    stmt = select(Playlist).options(
        selectinload(Playlist.songs).selectinload(Song.artists),
        selectinload(Playlist.songs).selectinload(Song.albums),
        selectinload(Playlist.songs).selectinload(Song.genres)
    ).filter_by(id=playlist_id,user_id=user_id)

    playlist = session.execute(stmt).scalar_one_or_none()

    if not playlist:
        return "Playlist not found"

    if not playlist.songs:
        return f"Playlist has no songs."

    playlist_details = {
        "playlist_id": playlist.id,
        "playlist_name": playlist.name,
        "songs": []
    }

    for song in playlist.songs:
        song_info = {
            "id": song.id,
            "name": song.name,
            "release_year": song.release_date,
            "artists": [artist.name for artist in song.artists],
            "albums": [album.name for album in song.albums] if song.albums else [],
            "genres": [genre.name for genre in song.genres] if song.genres else []
        }
        playlist_details["songs"].append(song_info)

    return playlist_details