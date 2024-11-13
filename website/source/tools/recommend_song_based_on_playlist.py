
from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Playlist, Song, get_current_user, session_maker, song_genre
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


@tool
def recommend_song_based_on_playlist(
    playlist_id: Annotated[int, "playlist id"]
) -> Annotated[list, "list of recommended songs"]:
    """This function recommends songs based on users playlist"""

    # print(f"CALLED ADD SONG TO PLAYLIST: SONG_ID {song_id} , playlist_id: {playlist_id}")
    user = get_current_user()

    try:
        return find_similar_songs(playlist_id,user.id)
    except Exception as exception:
        print(exception)
        return "Function call failed"


def find_similar_songs(playlist_id, user_id):
    session = session_maker()

    # Fetch the user's playlist
    stmt = select(Playlist).filter_by(id=playlist_id, user_id=user_id)
    playlist = session.execute(stmt).scalars().first()

    # If the playlist or songs are empty, return an empty list
    if playlist is None or not playlist.songs:
        return []

    # Calculate genre frequency in the playlist's songs
    genre_counts = {}
    for song in playlist.songs:
        for genre in song.genres:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    # Find the most popular genre
    most_popular_genre = max(genre_counts, key=genre_counts.get)
    # ignored_song_ids = [id for id in playlist.songs]

    # Query for songs with the most popular genre
    song_stmt = (
        select(Song)
        .options(selectinload(Song.genres))
        .options(selectinload(Song.artists))
        .join(song_genre)
        .where(song_genre.c.genre_id == most_popular_genre.id)
        # .where(~Song.id.in_(ignored_song_ids))
        .limit(10)
    )

    songs = session.execute(song_stmt).scalars().all()

    songs = [{"song_id": song.id, "name": song.name, "genre": song.genres} for song in songs]
    return songs

