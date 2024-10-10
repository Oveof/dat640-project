from source.db import clear_playlist, list_playlist, playlist_add_song, playlist_remove_song, new_user


def handle_nonempty_user_input(text):

    input_text = text.split(" ")  # Filter out no alphabetical characters

    cmd = input_text[0]

    NOT_RECOGNIZED = "Command does not exist"
    MALFORMED_COMMAND = "Commands should start with /"


    if cmd[0] != '/':
        return MALFORMED_COMMAND

    cmd = str(cmd[1:]).strip()


    command_descriptions = {
        "add" : "Add a song to a playlist",
        "remove": "Remove a song from a playlist",
        "list" : "List all songs in a playlist",
        "clear" : "Delete all songs from the playlist",
        "help" : "Print this message"
    }

    def print_help(_args):
        text=""
        for key,value in command_descriptions.items():
            text+=f"/{key} : {value} \n"

        return text

    command_functions = {
        "add" : playlist_add_song,
        "remove": playlist_remove_song,
        "list" : list_playlist,
        "clear" : clear_playlist,
        "help" : print_help
    }


    action = command_functions.get(cmd)
    print(f"DEBUG IS: {action}   ---------------------")

    if action!=None:
        return action(input_text[1:])


    return NOT_RECOGNIZED






# @app.route('/nlp', methods=['POST'])
# def process_input():
#     input_text = None

#     if 'text' not in request.form:
#         return "ERROR"
#     input_text = request.form['text'].split(" ")  # Filter out no alphabetical characters

#     cmd = input_text[0]


#     html = "<div class='responses'>"

#     all_commands = [("/add", "Adds to playlist"),
#                     ("/remove", "Removes from playlist"),
#                     ("/list", "List playlist"),
#                     ("/clear", "Clears playlist")]

#     match cmd:
#         case "/add":
#             arguments = ''.join(input_text[1:])
#             song_name = arguments.split("-")[0]
#             artist_name = arguments.split("-")[1]
#             response = playlist_add_song(session["user"], "default", song_name, artist_name)
#             html += response
#         case "/remove":
#             arguments = ''.join(input_text[1:])
#             song_name = arguments.split("-")[0]
#             artist_name = arguments.split("-")[1]
#             response = playlist_remove_song(session["user"], "default", song_name, artist_name)
#             html += response
#         case "/list":
#             playlist = list_playlist(session["user"], "default")
#             if playlist is not None:
#                 html += render_playlist(playlist)
#         case "/clear":
#             response = clear_playlist(session["user"], "default")
#             html += response
#         case "/help":
#             html += "<ul>"
#             for command, explanation in all_commands:
#                 html += f"<li>{command} - {explanation}"
#             html += "</ul>"
#         case _:
#             html += "<p>Unknown command</p>"
#     html+="</div>"
#     return html

