import json
from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Artist, Playlist, Song, User, get_current_user, song_artists, session_maker

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload

@tool
def delete_playlist(
    playlist_id: Annotated[int, "id of the playlist"]
) -> Annotated[str, "message, containing information on result of query"]:
    """Deletes a playlist based on id"""

    user = get_current_user()
    session = session_maker()

    stmt = select(Playlist).filter_by(id=playlist_id,user_id=user.id)
    playlist = session.execute(stmt).scalars().first()

    if not playlist:
        return f"Playlist with id '{playlist_id}' not found for this user."

    session.delete(playlist)
    session.commit()

    return f"Playlist with id '{playlist_id}' has been deleted."
