import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from accelerate import Accelerator, load_checkpoint_and_dispatch

import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')

from huggingface_hub import login

login(token=HF_TOKEN)

model_name = "mistralai/Mistral-7B-Instruct-v0.3"


from transformers import AutoModelForCausalLM, AutoTokenizer

local_cache_dir = "./local_model_cache"

# Download and load the model and tokenizer to the specified directory
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", cache_dir=local_cache_dir)
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=local_cache_dir)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  # Set pad token if not already set
model.config.pad_token_id = tokenizer.pad_token_id

def prompt_ai(prompt):

    messages = [
        {"role": "system", "content": """
            You are a natural language processor, you take text from a user and turn it into commands, below is a list of commands you support, if you dont have enough information for a command reply with /ins.
            /add <song name or id> <playlist name or id>
            /list <playlist name or id>
            /search <something to search with>
            /clear <playlist name or id>
            /remove <song name or id> <playlist name or id>
            /help <explain what you can do>

            Output must be in the form of a single word and context. Output must be structured example:
            Example for add:
                User: save Espresso to my playlist
                Output: /add <espresso> <my playlist>

            Example for add with playlist id:
                User: I'd like Espresso in 1
                Output: /add <espresso> <1>

            Example for add with song id:
                User: song 543 to my playlist
                Output: /add <543> <my playlist>

            Example for list, but there is not enough information on what to list:
                User: list my songs
                Output: /ins

        """},
        {"role": "user", "content": "discard espresso from my playlist"},
        {"role": "assistant", "content": "/remove <espresso> <my playlist>"},

        {"role": "user", "content": prompt},

    ]

    model_inputs = tokenizer(
        [msg['content'] for msg in messages],
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=1000
    )

    generated_ids = model.generate(
        input_ids=model_inputs['input_ids'],
        attention_mask=model_inputs['attention_mask'],
        max_new_tokens=100,
        pad_token_id=model.config.pad_token_id,
        do_sample=True
    )

    print(tokenizer.decode(generated_ids[0], skip_special_tokens=True))
    # print(tokenizer.batch_decode(generated_ids)[0])
    


print(prompt_ai("kick song 543 from 1"))

# print(prompt_ai("i'd like espresso in something awesome"))

# print(prompt_ai("do you have the song from titanic"))

