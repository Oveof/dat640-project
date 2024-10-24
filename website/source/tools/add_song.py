from langchain_core.tools import tool
from typing import Annotated, List
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage



@tool
def add_song_to_playlist(
    song_id: Annotated[int, "song id"],
    playlist_id: Annotated[int, "playlist id"]
    ) -> Annotated[bool, "True or False, means success or failure to add song."]:
    """Add a song to a playlist"""

    return True
add_song_to_playlist_examples = [
    HumanMessage(
        "Add the song 'Happy' to the playlist 'Feel Good Hits'", name="example_user"
    ),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            { "name": "search_song", "args": {"song_title": "Happy"}, "id": "1" }
        ],
    ),
    ToolMessage(
        """[
            { "id": 231, "name": "Happy", "artist": "Pharrell Williams", "release": "21.11.2023", "genre": ["Soul", "R&B"] },
            { "id": 99, "name": "Happy Now", "artist": "Kygo", "release": "12.07.2021", "genre": ["Pop", "Electronic"] }
        ]""", 
        tool_call_id="1"
    ),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            { "name": "list_user_playlists", "args": {}, "id": "2" }
        ],
    ),
    ToolMessage(
        """[
            { "id": 12, "name": "Feel Good Hits" },
            { "id": 5, "name": "Chill Vibes" }
        ]""",
        tool_call_id="2"
    ),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            { "name": "add_song_to_playlist", "args": {"song_id": 231, "playlist_id": 12}, "id": "3" }
        ],
    ),
    ToolMessage("True", tool_call_id="3"),
    AIMessage(
        """I successfully added 'Happy' by Pharrell Williams to the playlist 'Feel Good Hits'.""",
        name="example_assistant",
    ),

    HumanMessage(
        "Add the song 'Bohemian Rhapsody' to the playlist 'Classic Rock'", name="example_user2"
    ),
    AIMessage(
        "",
        name="example_assistant2",
        tool_calls=[
            { "name": "search_song", "args": {"song_title": "Bohemian Rhapsody"}, "id": "4" }
        ],
    ),
    ToolMessage(
        """[
            { "id": 123, "name": "Bohemian Rhapsody", "artist": "Queen", "release": "31.10.1975", "genre": ["Rock"] }
        ]""",
        tool_call_id="4"
    ),
    AIMessage(
        "",
        name="example_assistant2",
        tool_calls=[
            { "name": "list_user_playlists", "args": {}, "id": "5" }
        ],
    ),
    ToolMessage(
        """[
            { "id": 7, "name": "Classic Rock" },
            { "id": 8, "name": "Workout Jams" }
        ]""",
        tool_call_id="5"
    ),
    AIMessage(
        "",
        name="example_assistant2",
        tool_calls=[
            { "name": "add_song_to_playlist", "args": {"song_id": 123, "playlist_id": 7}, "id": "6" }
        ],
    ),
    ToolMessage("True", tool_call_id="6"),
    AIMessage(
        """I successfully added 'Bohemian Rhapsody' by Queen to the playlist 'Classic Rock'.""",
        name="example_assistant2",
    ),

    HumanMessage(
        "Add the song 'Nonexistent Song' to the playlist 'Chill Vibes'", name="example_user3"
    ),
    AIMessage(
        "",
        name="example_assistant3",
        tool_calls=[
            { "name": "search_song", "args": {"song_title": "Nonexistent Song"}, "id": "7" }
        ],
    ),
    ToolMessage("[]", tool_call_id="7"),
    AIMessage(
        """I was unable to find any song matching 'Nonexistent Song'. Please check the song name and try again.""",
        name="example_assistant3",
    ),
]
