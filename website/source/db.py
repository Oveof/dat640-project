from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import ForeignKey, MetaData, UniqueConstraint
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
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import session as flask_session
import json

class Base(DeclarativeBase):
    pass

NAME_LENGTH = 1024
SESSION_LENGTH = 32

playlist_song = Table(
    "playlist_song",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlists.id"), nullable=False),
    Column("song_id", ForeignKey("songs.id"),  nullable=False),
    Column("position", Integer(),nullable=False, autoincrement=True),
    UniqueConstraint("playlist_id","position"),
)

song_artists = Table(
    "song_artists",
    Base.metadata,
    Column("artist_id", ForeignKey("artists.id"), nullable=False),
    Column("song_id", ForeignKey("songs.id"),  nullable=False),
    UniqueConstraint("artist_id","song_id")
)

song_genre = Table(
    "song_genre",
    Base.metadata,
    Column("genre_id", ForeignKey("genres.id"), nullable=False),
    Column("song_id", ForeignKey("songs.id"),  nullable=False),
    UniqueConstraint("genre_id","song_id")
)

song_album = Table(
    "song_album",
    Base.metadata,
    Column("album_id", ForeignKey("albums.id"), nullable=False),
    Column("song_id", ForeignKey("songs.id"),  nullable=False),
    UniqueConstraint("album_id","song_id")
)
class Artist(Base):
    __tablename__ = "artists"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)

class Album(Base):
    __tablename__ = "albums"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    release_date:Mapped[int] = mapped_column(Integer,nullable=True)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "release_date": self.release_date
        }

class Song(Base):
    __tablename__ = "songs"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    # compare_name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    artists: Mapped[list[Artist]] = relationship(secondary=song_artists)
    # album: Mapped[int] = mapped_column(ForeignKey("albums.id"), nullable=False)
    albums: Mapped[list[Album]] = relationship(secondary=song_album)
    genres: Mapped[list[Genre]] = relationship(secondary=song_genre)
    release_date: Mapped[int] = mapped_column(Integer,nullable=True)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "release_year": self.release_date,
            "artists": [artist.to_dict() for artist in self.artists],
            "albums": [album.to_dict() for album in self.albums]
        }


class Playlist(Base):
    __tablename__ = "playlists"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    songs: Mapped[list[Song]] = relationship(secondary=playlist_song)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_LENGTH))
    user_session: Mapped[str] = mapped_column(String(SESSION_LENGTH), nullable=False, unique=True)
    playlists: Mapped[List[Playlist]] = relationship()

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


def create_user(user_session: str, name: str):
    session = session_maker()
    new_user = User(user_session=user_session, name=name)
    session.add(new_user)
    session.commit()
    session.commit()


def get_current_user()->User:
    session = session_maker()
    session_id = flask_session.get("user", None)
    if session_id==None:
        return "No session"
    user = session.query(User).filter_by(user_session=session_id).first()
    if user == None:
        create_user(session_id,'')
    return user





    
#     new_user("bruh", "ove")
#     playlist_add_song("bruh", "my_playst", "Never gonna give you up", "Rick Astley")
#     # playlist_remove_song("bruh", "my_playst", "Never gonna give you up")
#     print(list_playlist("bruh", "my_playst"))

