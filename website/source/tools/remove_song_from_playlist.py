from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Playlist, Song, get_current_user, session_maker


@tool
def remove_song_from_playlist(
    song_id: Annotated[int, "song id"],
    playlist_id: Annotated[int, "playlist id"]
) -> Annotated[str, "Informational error, or success message"]:
    """Remove a song from a user's playlist"""

    user = get_current_user()

    try:
        return db_remove_song_from_playlist(song_id,playlist_id,user.id)
    except Exception as exception:
        print(exception)
        return "Function call failed"


def db_remove_song_from_playlist(song_id,playlist_id,user_id):
    session = session_maker()

    playlist = session.query(Playlist).filter_by(id=playlist_id, user_id=user_id).first()

    if not playlist:
        return "Playlist not found"

    song = session.query(Song).filter_by(id=song_id).first()

    if not song:
        return "That song is not in the database"

    if song not in playlist.songs:
        return "Song was not in playlist"

    playlist.songs.remove(song)

    session.commit()

    return "Successfully removed song"
