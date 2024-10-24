import json
from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from source.db import Artist, Playlist, Song, User, get_current_user, song_artists, session_maker

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload

@tool
def create_playlist(
    playlist_name: Annotated[str, "Name of the playlist"],
    ) -> Annotated[str, "message, containing information on result"]:
    """Create a playlist"""
    
    print("CALLED CREATE PLAYLIST")

    user = get_current_user()

    return create_playlist(playlist_name,user.id)



def db_create_playlist(playlist_name,user_id):
    session = session_maker()

    new_playlist = Playlist(name=playlist_name, user_id=user_id, songs=[])
    session.add(new_playlist)
    session.commit()

    return "Successfully created playlist"

if __name__ == "__main__":
    print(create_playlist("raid"))