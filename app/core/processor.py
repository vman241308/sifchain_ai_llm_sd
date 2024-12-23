import app.core.memory_management as memory_management
import time
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from transformers.generation.stopping_criteria import StoppingCriteriaList
from threading import Thread
import app.core.canvas as sifchain_canvas
import json

HF_TOKEN = None
history = []

llm_name = 'lllyasviel/omost-llama-3-8b-4bits'

llm_model = AutoModelForCausalLM.from_pretrained(
    llm_name,
    torch_dtype=torch.bfloat16,  # This is computation type, not load/memory type. The loading quant type is baked in config.
    token=HF_TOKEN,
    device_map="auto"  # This will load model to gpu with an offload system
)

llm_tokenizer = AutoTokenizer.from_pretrained(
    llm_name,
    token=HF_TOKEN
)

def chat_fn(message: str, history: list, seed:int, temperature: float, top_p: float, max_new_tokens: int, system_prompt: str) -> str:
    np.random.seed(int(seed))
    torch.manual_seed(int(seed))

    conversation = [{"role": "system", "content": system_prompt}]

    for user, assistant in history:
        if isinstance(user, str) and isinstance(assistant, str):
            if len(user) > 0 and len(assistant) > 0:
                conversation.extend([{"role": "user", "content": user}, {"role": "assistant", "content": assistant}])

    conversation.append({"role": "user", "content": message})

    memory_management.load_models_to_gpu(llm_model)

    input_ids = llm_tokenizer.apply_chat_template(
        conversation, return_tensors="pt", add_generation_prompt=True).to(llm_model.device)

    streamer = TextIteratorStreamer(llm_tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True)

    def interactive_stopping_criteria(*args, **kwargs) -> bool:
        if getattr(streamer, 'user_interrupted', False):
            print('User stopped generation')
            return True
        else:
            return False

    stopping_criteria = StoppingCriteriaList([interactive_stopping_criteria])

    def interrupter():
        streamer.user_interrupted = True
        return

    generate_kwargs = dict(
        input_ids=input_ids,
        streamer=streamer,
        stopping_criteria=stopping_criteria,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=top_p,
    )

    if temperature == 0:
        generate_kwargs['do_sample'] = False

    Thread(target=llm_model.generate, kwargs=generate_kwargs).start()

    outputs = []
    for text in streamer:
        outputs.append(text)
        # print(outputs)
        yield "".join(outputs), interrupter

    return outputs

def save_chat_history(role, content):
    history.append({"role": role, "content": content})

def process_input(content, file):
    save_chat_history("user", content)
    # seed = torch.Generator(device="cuda").manual_seed(int(time.time() * 1000) % 2**32)
    system_prompt = "You are a helpful AI assistant"
    llm_generator = chat_fn(message=content, history=history, seed=int(time.time() * 1000) % 2**32, temperature=0.7, top_p=1, max_new_tokens=4096, system_prompt=system_prompt)
    
    final_response = ""
    for response_chunk, interrupter in llm_generator:
        final_response = response_chunk  # This will keep updating until the generator is exhausted
    
    print("~~~~~~~~~~~~~~~~~~~final_response:", final_response)    
    save_chat_history("assistant", final_response)

    paired_history = []
    if history:
        temp_history = []
        # Convert the list of dicts into pairs of messages
        for his in history:
            temp_history.append(his["content"])

            if len(temp_history) == 2:
                paired_history.append(temp_history)
                temp_history = []
    print("~~~~~~~~~~~~~~~~~~~paired_history:", paired_history)
    return paired_history

def format_chat_history():
    formatted_history = []
    for i in range(0, len(history), 2):
        if i + 1 < len(history):
            user_content = history[i]["content"]
            assistant_content = history[i + 1]["content"]
            formatted_history.append((user_content, assistant_content))
    return formatted_history

def process_json():
    canvas_outputs = None
    system_prompt = sifchain_canvas.system_prompt
    try:
        if history:
            custom_history = format_chat_history()
            last_assistant = custom_history[-1][1] if len(custom_history) > 0 else None
            llm_generator = chat_fn(message=last_assistant, history=history, seed=int(time.time() * 1000) % 2**32, temperature=0.7, top_p=1, max_new_tokens=4096, system_prompt=system_prompt)
            final_response = ""
            for response_chunk, interrupter in llm_generator:
                final_response = response_chunk  # This will keep updating until the generator is exhausted
            # canvas = sifchain_canvas.Canvas.from_bot_response(final_response)
            # canvas_outputs = canvas.process()
            canvas_outputs = final_response
    except Exception as e:
        print('Last assistant response is not valid canvas:', e)

    print("~~~~~~~~~~~~~~~~~~~canvas_outputs:", canvas_outputs)
    # return canvas_outputs, gr.update(visible=canvas_outputs is not None), gr.update(interactive=len(history) > 0)
    return canvas_outputs
