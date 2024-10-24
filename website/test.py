from source.tools.add_song_to_playlist import db_add_song_to_playlist
from source.tools.create_playlist import db_create_playlist
from source.tools.delete_playlist import db_delete_playlist
from source.tools.remove_song_from_playlist import db_remove_song_from_playlist





assert db_create_playlist("TESTING_PLAYLIST",0) == "Successfully created playlist"
assert db_delete_playlist(10000000,0) == "Playlist not found"
assert db_delete_playlist(1,0) == "Playlist deleted"


assert db_create_playlist("TESTING_PLAYLIST",0) == "Successfully created playlist"

assert db_add_song_to_playlist(1,100,0) == "Playlist not found"
assert db_add_song_to_playlist(10000000,1,0) == "Song not found"
assert db_add_song_to_playlist(1,1,0) == "Success"


assert db_remove_song_from_playlist(10000000,1,0) == "That song is not in the database"
assert db_remove_song_from_playlist(1,100,0) == "Playlist not found"
assert db_remove_song_from_playlist(10,1,0) == "Song was not in playlist"
assert db_remove_song_from_playlist(1,1,0) == "Successfully removed song"
assert db_delete_playlist(1,0) == "Playlist deleted"


assert db_create_playlist("TESTING_PLAYLIST",0) == "Successfully created playlist"
assert db_add_song_to_playlist(1,1,0) == "Success"
assert db_delete_playlist(1,0) == "Playlist deleted"






