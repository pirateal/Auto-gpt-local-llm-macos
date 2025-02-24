import tiktoken
from typing import List, Dict


def count_message_tokens(messages : List[Dict[str, str]], model : str = "gpt-3.5-turbo-0301") -> int:
    """
    Returns the number of tokens used by a list of messages.

    Args:
    messages (list): A list of messages, each of which is a dictionary containing the role and content of the message.
    model (str): The name of the model to use for tokenization. Defaults to "gpt-3.5-turbo-0301".

    Returns:
    int: The number of tokens used by the list of messages.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warn("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        # !Node: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return count_message_tokens(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        # !Note: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return count_message_tokens(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def count_string_tokens(string: str, model_name: str) -> int:
    """
    Returns the number of tokens in a text string.

    Args:
    string (str): The text string.
    model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
    int: The number of tokens in the text string.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# Modified for enhanced functionality

# Modified for enhanced functionality


# Updated model configuration
model_config = {
    "name": "Exported from LM Studio on 12/28/2023, 1:52:38 PM",
    "load_params": {
        "n_ctx": 4000,
        "n_batch": 512,
        "rope_freq_base": 0,
        "rope_freq_scale": 0,
        "n_gpu_layers": 3000,
        "use_mlock": True,
        "main_gpu": 0,
        "tensor_split": [
            0
        ],
        "seed": -1,
        "f16_kv": True,
        "use_mmap": True
    },
    "inference_params": {
        "n_threads": 8,
        "n_predict": -1,
        "top_k": 40,
        "top_p": 0.95,
        "temp": 0.2,
        "repeat_penalty": 1.1,
        "input_prefix": "[INST]",
        "input_suffix": "[/INST]",
        "antiprompt": [
            "[INST]"
        ],
        "pre_prompt": "Below is an instruction that describes a task. Write a response that appropriately completes the request.",
        "pre_prompt_suffix": "\\n<</SYS>>\\n\\n[/INST]",
        "pre_prompt_prefix": "[INST]<<SYS>>\\n",
        "seed": -1,
        "tfs_z": 1,
        "typical_p": 1,
        "repeat_last_n": 64,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "n_keep": 0,
        "logit_bias": {},
        "mirostat": 0,
        "mirostat_tau": 5,
        "mirostat_eta": 0.1,
        "memory_f16": True,
        "multiline_input": False,
        "penalize_nl": True
    }
}