from llm_utils import create_chat_completion

next_key = 0
agents = {}  # key, (task, full_message_history, model)

# Create new GPT agent
# TODO: Centralise use of create_chat_completion() to globally enforce token limit


def create_agent(task, prompt, model):
    """Create a new agent and return its key"""
    global next_key
    global agents

    if not prompt.strip():
        raise ValueError("The prompt cannot be empty")
    messages = [{"role": "user", "content": prompt}, ]

    # Start GPT instance
    agent_reply = create_chat_completion(
        model=model,
        messages=messages,
    )

    # Update full message history
    if not agent_reply.strip():
        raise ValueError("The agent reply cannot be empty")
    messages.append({"role": "assistant", "content": agent_reply})

    key = next_key
    # This is done instead of len(agents) to make keys unique even if agents
    # are deleted
    next_key += 1

    agents[key] = (task, messages, model)

    return key, agent_reply


def message_agent(key, message):
    """Send a message to an agent and return its response"""
    global agents

    task, messages, model = agents[int(key)]

    # Add user message to message history before sending to agent
    messages.append({"role": "user", "content": message})

    # Start GPT instance
    agent_reply = create_chat_completion(
        model=model,
        messages=messages,
    )

    # Update full message history
    if not agent_reply.strip():
        raise ValueError("The agent reply cannot be empty")
    messages.append({"role": "assistant", "content": agent_reply})

    return agent_reply


def list_agents():
    """Return a list of all agents"""
    global agents

    # Return a list of agent keys and their tasks
    return [(key, task) for key, (task, _, _) in agents.items()]


def delete_agent(key):
    """Delete an agent and return True if successful, False otherwise"""
    global agents

    try:
        del agents[int(key)]
        return True
    except KeyError:
        return False

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