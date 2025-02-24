import requests
import io
import os.path
from PIL import Image
from config import Config
import uuid
import openai
from base64 import b64decode

cfg = Config()

working_directory = "auto_gpt_workspace"


def generate_image(prompt):

    filename = str(uuid.uuid4()) + ".jpg"

    # DALL-E
    if cfg.image_provider == 'dalle':

        openai.api_key = cfg.openai_api_key

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256",
            response_format="b64_json",
        )

        print("Image Generated for prompt:" + prompt)

        image_data = b64decode(response["data"][0]["b64_json"])

        with open(working_directory + "/" + filename, mode="wb") as png:
            png.write(image_data)

        return "Saved to disk:" + filename

    # STABLE DIFFUSION
    elif cfg.image_provider == 'sd':

        API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
        headers = {"Authorization": "Bearer " + cfg.huggingface_api_token}

        response = requests.post(API_URL, headers=headers, json={
            "inputs": prompt,
        })

        image = Image.open(io.BytesIO(response.content))
        print("Image Generated for prompt:" + prompt)

        image.save(os.path.join(working_directory, filename))

        return "Saved to disk:" + filename

    else:
        return "No Image Provider Set"

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