from promptgenerator import PromptGenerator


def get_prompt():
    """
    This function generates a prompt string that includes various constraints, commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint("~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.")
    prompt_generator.add_constraint("If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.")
    prompt_generator.add_constraint("No user assistance")
    prompt_generator.add_constraint('Exclusively use the commands listed in double quotes e.g. "command name"')

    # Define the command list
    commands = [
        ("Google Search", "google", {"input": "<search>"}),
        ("Browse Website", "browse_website", {"url": "<url>", "question": "<what_you_want_to_find_on_website>"}),
        ("Start GPT Agent", "start_agent", {"name": "<name>", "task": "<short_task_desc>", "prompt": "<prompt>"}),
        ("Message GPT Agent", "message_agent", {"key": "<key>", "message": "<message>"}),
        ("List GPT Agents", "list_agents", {}),
        ("Delete GPT Agent", "delete_agent", {"key": "<key>"}),
        ("Write to file", "write_to_file", {"file": "<file>", "text": "<text>"}),
        ("Read file", "read_file", {"file": "<file>"}),
        ("Append to file", "append_to_file", {"file": "<file>", "text": "<text>"}),
        ("Delete file", "delete_file", {"file": "<file>"}),
        ("Search Files", "search_files", {"directory": "<directory>"}),
        ("Evaluate Code", "evaluate_code", {"code": "<full_code_string>"}),
        ("Get Improved Code", "improve_code", {"suggestions": "<list_of_suggestions>", "code": "<full_code_string>"}),
        ("Write Tests", "write_tests", {"code": "<full_code_string>", "focus": "<list_of_focus_areas>"}),
        ("Execute Python File", "execute_python_file", {"file": "<file>"}),
        ("Execute Shell Command, non-interactive commands only", "execute_shell", { "command_line": "<command_line>"}),
        ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
        ("Generate Image", "generate_image", {"prompt": "<prompt>"}),
        ("Do Nothing", "do_nothing", {}),
    ]

    # Add commands to the PromptGenerator object
    for command_label, command_name, args in commands:
        prompt_generator.add_command(command_label, command_name, args)

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource("Internet access for searches and information gathering.")
    prompt_generator.add_resource("Long Term memory management.")
    prompt_generator.add_resource("GPT-3.5 powered Agents for delegation of simple tasks.")
    prompt_generator.add_resource("File output.")

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation("Continuously review and analyze your actions to ensure you are performing to the best of your abilities.")
    prompt_generator.add_performance_evaluation("Constructively self-criticize your big-picture behavior constantly.")
    prompt_generator.add_performance_evaluation("Reflect on past decisions and strategies to refine your approach.")
    prompt_generator.add_performance_evaluation("Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.")

    # Generate the prompt string
    prompt_string = prompt_generator.generate_prompt_string()

    return prompt_string

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
def get_pre_prompt():
    return "Welcome! You are now interacting with the AI. Please provide your commands or ask questions."
