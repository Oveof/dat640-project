import torch

from transformers import AutoTokenizer, AutoModelForCausalLM,GPTQConfig
from accelerate import Accelerator, load_checkpoint_and_dispatch

import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')

from huggingface_hub import login
login(token=HF_TOKEN)

model_name = "mistralai/Mistral-7B-Instruct-v0.3"
model_name = "neuralmagic/Mistral-7B-Instruct-v0.3-quantized.w8a16"

local_cache_dir ="./local_model_cache"
local_cache_dir_quantized ="./local_model_cache/local_model_cache_quantized"
quantized_model_path = local_cache_dir_quantized+"/Mistral_7B_Instruct_v0.3_quantized.sdict"
accelerator = Accelerator()

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=local_cache_dir,
    device_map="cuda",
    torch_dtype=torch.float16
)


#model = torch.quantization.quantize_dynamic(
#    model,  # the original model
#    {torch.nn.Linear},  # layers to quantize
#    dtype=torch.qint8  # data type for quantization (int8)
#)
#model = None
#model = AutoModddelForCausalLM.from_pretrained(
#    model_name,
#    cache_dir=local_cache_dir,
#    device_map="cpu",
#    torch_dtype=torch.float16)

#model.to(torch.float32)
tokenizer = AutoTokenizer.from_pretrained(model_name)

#gptq_config = GPTQConfig(bits=2, dataset="c4", tokenizer=tokenizer)

# Load and quantize the model
#quantized_model = AutoModelForCausalLM.from_pretrained(
#    model_name,
#    cache_dir=local_cache_dir,
#    device_map="cpu",
#    quantization_config=gptq_config,
#    torch_dtype=torch.float16
#)


#model = quantized_model
#model.to(torch.float16)
#model.to('cuda')


#tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=local_cache_dir)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id

model = accelerator.prepare(model)

def prompt_ai(prompt):
    # System prompt giving clear instructions on expected output format
    system_prompt = f"""
<s>[INST]
You have access to interact with a database to either provide informational responses or execute system commands, depending on the user's input.
You must reply with either an answer or a command based on the nature of the request.
Below are the commands you support:
- /add <song name or id> <playlist name or id>
- /list <playlist name or id>
- /search <song title search>
- /clear <playlist name or id>
- /remove <song name or id> <playlist name or id>
- /repl <informational message>

Rules:
1. If the user asks for general information or makes a query that expects an answer (e.g., asking for song details, suggestions), reply with a /repl command containing the actual answer or suggestion (e.g., the name of a movie song, playlist details).
2. If the user asks for an action (e.g., adding, listing, searching), respond with the appropriate system command.
3. If the user explicitly says "search" or "find", you may use the /search command.
4. For help requests, reply with a /repl command that provides information about your functionality.
5. Respond with the command or answer in the format provided without any placeholders.
6. If you do not have enough information for a query, you may use the /relp command and ask the user for more information.
7. Cater to the user's query by providing actual suggestions when applicable.

Examples:
User: song 543 to my playlist
Output: /add <543> <my playlist>

User: clear my songs
Output: /ins

User: suggest a movie song
Output: /repl <You may enjoy 'My Heart Will Go On' from Titanic.>

User: what are my playlists
Output: /list <your playlists>

User: do you know any movie songs?
Output: /repl <Yes, you might like 'Shallow' from A Star is Born.>

For the following user input:
{prompt}
Reply with only the correct command or actual information, without placeholders.
[/INST]</s>"""


    # Tokenize user input for model
    model_inputs = tokenizer(
        system_prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )

    # Ensure input_ids are on the correct device
    model_inputs = {k: v.to(model.device) for k, v in model_inputs.items()}

    with accelerator.autocast():
        generated_ids = model.generate(
            input_ids=model_inputs['input_ids'],
            attention_mask=model_inputs['attention_mask'],
            max_new_tokens=500,
            pad_token_id=model.config.pad_token_id,
            do_sample=False  # Disable sampling for deterministic behavior
        )

    # # Return only the generated command without extra information
    # output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    # return output.strip()

    output = tokenizer.decode(generated_ids[0], skip_special_tokens=False)
    return output.strip().split("[/INST]")[-1][:-4]

# print(prompt_ai("kick song 543 from 1"))
