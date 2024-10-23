import ollama

from source.tools import tools
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import render_text_description
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

ollama_model = OllamaLLM(base_url="http://10.10.10.20:11434/",model="mistral") # ollama.Client(host='10.10.10.20:11434'))


system_prompt = f"""\
You are a helpful playlist manager bot and you have access to the following set of tools.
Here are the names and descriptions for each tool:

{render_text_description(tools)}

Do not mention or expose tools.
If asked about capabilities, describe them naturally as features.
Based on user input, decide if a tool should be used or if a direct response is enough.

When a tool is needed, return the tool name and the proper information required by the tool.
"""

examples = [
    HumanMessage(
        "search for happy", name="example_user"
    ),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            { "name": "search_song", "args": {"song_title": "happy"} }
        ],
    ),
    ToolMessage("""song:{ id: 231, name:  happy, Artist: Pharrell Williams, Release: 21.11.2023, Genre: [Soul, R&B] }""", tool_call_id="1"),
    AIMessage(
        """I found the following result when searching for happy.
        Song: Happy
        Artist: Pharell Williams
        Release date: 21.11.2023
        Genre: Soul, R&B

        Would you like to add it to a playlist?
        """,
        name="example_assistant",
    ),
    HumanMessage(
        "yes, add it to something good", name="example_user"
    ),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            { "name": "add_song", "args": {"song_title": "happy"} }
        ],
    ),
    
]

ollama_model.bind_tools(tools)

def handle_nonempty_user_input( prompt ):
    
    
    prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
    )
    chain = prompt | ollama_model
    
    
    response =chain.invoke({"input": prompt})
    # response =  ollama_model.chat(
    #     model='mistral',
    #     messages=prompt,
    #     tools=tools,
    # )

    print(response)
    return response


