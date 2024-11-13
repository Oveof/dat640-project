from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import (
    Base, User, Playlist, Song, Album, Artist, Genre, playlist_song, song_artists, song_genre, song_album
)

# Set up the engine for the old and new databases
old_engine = create_engine("sqlite:///old_old_sqlite.db")  # Change this to your old SQLite file
new_engine = create_engine("sqlite:///new_sqlite.db")  # Change this to your new SQLite file

# Create sessions for both databases
OldSession = sessionmaker(bind=old_engine)
NewSession = sessionmaker(bind=new_engine)
old_session = OldSession()
new_session = NewSession()

# Create all tables in the new database
Base.metadata.create_all(new_engine)

# Function to copy data from old database to new one
def migrate_users():
    old_users = old_session.query(User).all()
    for old_user in old_users:
        # Expunge the object from old session
        old_session.expunge(old_user)
        new_user = User(
            id=old_user.id,
            name=old_user.name,
            user_session=old_user.user_session,
            playlists=[]  # Relationships handled separately
        )
        new_session.add(new_user)
    new_session.commit()

def migrate_playlists():
    old_playlists = old_session.query(Playlist).all()
    for old_playlist in old_playlists:
        old_session.expunge(old_playlist)
        new_playlist = Playlist(
            id=old_playlist.id,
            name=old_playlist.name,
            user_id=old_playlist.user_id,
            songs=[]  # Relationships handled separately
        )
        new_session.add(new_playlist)
    new_session.commit()

def migrate_artists():
    old_artists = old_session.query(Artist).all()
    for old_artist in old_artists:
        old_session.expunge(old_artist)
        new_artist = Artist(
            id=old_artist.id,
            name=old_artist.name
        )
        new_session.add(new_artist)
    new_session.commit()

def migrate_genres():
    old_genres = old_session.query(Genre).all()
    for old_genre in old_genres:
        old_session.expunge(old_genre)
        new_genre = Genre(
            id=old_genre.id,
            name=old_genre.name
        )
        new_session.add(new_genre)
    new_session.commit()

def migrate_albums():
    old_albums = old_session.query(Album).all()
    for old_album in old_albums:
        old_session.expunge(old_album)
        new_album = Album(
            id=old_album.id,
            name=old_album.name,
            release_date=old_album.release_date
        )
        new_session.add(new_album)
    new_session.commit()

def migrate_songs():
    old_songs = old_session.query(Song).all()
    for old_song in old_songs:
        old_session.expunge(old_song)
        new_song = Song(
            id=old_song.id,
            name=old_song.name,
            artists=old_song.artists,  # Handle relationships separately to avoid session conflicts
            albums=old_song.albums,
            genres=old_song.genres
        )
        new_session.add(new_song)
    new_session.commit()

def migrate_playlist_songs():
    old_playlist_songs = old_session.execute(playlist_song.select()).fetchall()
    for row in old_playlist_songs:
        new_session.execute(playlist_song.insert().values(
            playlist_id=row['playlist_id'],
            song_id=row['song_id'],
        ))
    new_session.commit()

def migrate_song_artists():
    old_song_artists = old_session.execute(song_artists.select()).fetchall()
    for row in old_song_artists:
        new_session.execute(song_artists.insert().values(
            artist_id=row['artist_id'],
            song_id=row['song_id']
        ))
    new_session.commit()

def migrate_song_genres():
    old_song_genres = old_session.execute(song_genre.select()).fetchall()
    for row in old_song_genres:
        new_session.execute(song_genre.insert().values(
            genre_id=row['genre_id'],
            song_id=row['song_id']
        ))
    new_session.commit()

def migrate_song_albums():
    old_song_albums = old_session.execute(song_album.select()).fetchall()
    for row in old_song_albums:
        new_session.execute(song_album.insert().values(
            album_id=row['album_id'],
            song_id=row['song_id']
        ))
    new_session.commit()

# Migrate data in the correct order to maintain foreign key relationships
migrate_users()
migrate_artists()
migrate_genres()
migrate_albums()
migrate_songs()
migrate_playlists()
migrate_playlist_songs()
migrate_song_artists()
migrate_song_genres()
migrate_song_albums()

# Close the sessions
old_session.close()
new_session.close()
