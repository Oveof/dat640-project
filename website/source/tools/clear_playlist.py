import json
from langchain_core.tools import tool
from sqlalchemy import select
from typing import Annotated
from source.db import Playlist, get_current_user, session_maker

@tool
def clear_playlist(
    playlist_name: Annotated[str, "Name of the playlist"]
) -> Annotated[str, "message, containing information on result"]:
    """Clear all songs from a playlist"""

    print("CALLED CLEAR PLAYLIST")
    user = get_current_user()

    try:
        return db_clear_playlist(playlist_name,user.id)
    except Exception as exception:
        print(exception)
        return "Function call failed"



def db_clear_playlist(playlist_name,user_id):
    session = session_maker()
    stmt = select(Playlist).filter_by(name=playlist_name,user_id=user_id)
    playlist = session.execute(stmt).scalars().first()

    if not playlist:
        return f"Playlist '{playlist_name}' not found for this user."

    playlist.songs.clear()

    session.commit()

    return f"Playlist '{playlist_name}' has been cleared."