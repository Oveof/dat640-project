import ollama

# system_prompt = """
# You are a helpful assistant. When the user asks to sum two numbers, use the 'get_sum' function to provide the result.
# If the user asks a question that does not involve summing numbers, respond normally.
# """


ollama_model = ollama.Client(host='10.10.10.20:11434')

def get_sum(a: int, b: int) -> int:
    return a + b

user_prompt = "Please sum the numbers 4 and 7."

response = ollama_model.chat(
    model='mistral',
    messages=[{'role': 'user', 'content': 'What is the weather in Toronto?'}],

    tools=[{
      'type': 'function',
      'function': {
        'name': 'get_current_weather',
        'description': 'Get the current weather for a city',
        'parameters': {
          'type': 'object',
          'properties': {
            'city': {
              'type': 'string',
              'description': 'The name of the city',
            },
          },
          'required': ['city'],
        },
      },
    },
  ],
)

print(response['message']['tool_calls'])

print(response)



