from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Artist, Playlist, Song, User, get_current_user, song_artists, session_maker

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload


@tool
def list_playlists() -> Annotated[List[Annotated[str, "A list of the users playlists"]], "List of playlists for the current user"]:
    """List all playlists for the current user"""

    print("LIST PLAYLISTS WAS CALLED")
    user = get_current_user()
    session = session_maker()

    stmt = select(Playlist).filter_by(user_id=user.id)
    playlists = session.execute(stmt).scalars().all()

    if not playlists:
        return []

    playlist_details = [{"id": playlist.id, "name": playlist.name} for playlist in playlists]

    return playlist_details



