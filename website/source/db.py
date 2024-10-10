# from typing import List
# from typing import Optional
from sqlalchemy import ForeignKey, MetaData
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List, Optional

class Base(DeclarativeBase):
    pass


playlist_song = Table(
    "playlist_song",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlists.id")),
    Column("song_id", ForeignKey("songs.id")),
)
class Song(Base):
    __tablename__ = "songs"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    artist: Mapped[str] = mapped_column(String(30))
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

class Playlist(Base):
    __tablename__ = "playlists"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    songs: Mapped[list[Song]] = relationship(secondary=playlist_song)
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    user_session: Mapped[str] = mapped_column(String(30))
    playlists: Mapped[List[Playlist]] = relationship()
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


engine = create_engine("sqlite:///sqlite.db", echo=False)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)

def add_song(song_name: str, artist: str):
    session = session_maker()
    song = session.query(Song).filter_by(name=song_name, artist=artist).first()
    if song is None:
        song = Song(name=song_name, artist=artist)
        session.add(song)
        session.commit()

def remove_song(song_name: str, artist: str):
    session = session_maker()
    song = session.query(Song).filter_by(name=song_name, artist=artist).first()
    if song is not None:
        session.delete(song)
        session.commit()


def playlist_add_song(user_session: str, playlist_name: str, song_name: str, artist: str) -> str:
    session = session_maker()
    user = session.query(User).filter_by(user_session=user_session).first()
    if user == None:
        return "User does not exist"

    playlist = session.query(Playlist).filter_by(name=playlist_name, user_id=user.id).first()
    if playlist is None:
        playlist = Playlist(name=playlist_name, user_id=user.id)
        session.add(playlist)

    song = session.query(Song).filter_by(name=song_name).first()
    if song is None:
        song = Song(name=song_name, artist=artist)
        session.add(song)
    playlist.songs.append(song)

    session.commit()
    return "Successfully added song"

def playlist_remove_song(user_session: str, playlist_name: str, song_name: str, artist: str) -> str:
    session = session_maker()
    user = session.query(User).filter_by(user_session=user_session).first()
    if user is None:
        return "User does not exist"
    playlist = session.query(Playlist).filter_by(name=playlist_name, user_id=user.id).first()
    song = session.query(Song).filter_by(name=song_name, artist=artist).first()
    if playlist is None or song is None:
        return "Song or playlist does not exist"
    
    playlist.songs.remove(song)
    session.commit()
    return "Successfully removed song"

def list_playlist(user_session: str, playlist_name: str) -> Optional[list[tuple[str, str]]]:
    session = session_maker()
    user = session.query(User).filter_by(user_session=user_session).first()
    if user is None:
        return None
    playlist = session.query(Playlist).filter_by(name=playlist_name, user_id=user.id).first()
    if playlist is None:
        return None

    songs = []
    for song in playlist.songs:
        songs.append((song.name, song.artist))
    return songs

def clear_playlist(user_session: str, playlist_name: str) -> str:
    session = session_maker()
    user = session.query(User).filter_by(user_session=user_session).first()
    if user is None:
        return "User does not exist"

    playlist = session.query(Playlist).filter_by(name=playlist_name).first()
    if playlist is None:
        return "playlist does not exist"
    
    playlist.songs.clear()

    session.commit()
    return "Cleared playlist"
    


def new_user(user_session: str, name: str):
    session = session_maker()
    user = session.query(User).filter_by(user_session=user_session).first()
    if user is not None:
        print("user exists")
        return
    new_user = User(user_session=user_session, name=name)
    session.add(new_user)
    session.commit()









if __name__ == "__main__":
    new_user("bruh", "ove")
    playlist_add_song("bruh", "my_playst", "Never gonna give you up", "Rick Astley")
    # playlist_remove_song("bruh", "my_playst", "Never gonna give you up")
    print(list_playlist("bruh", "my_playst"))

