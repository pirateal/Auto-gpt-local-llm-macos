
import pinecone

from memory.base import MemoryProviderSingleton, get_ada_embedding
from logger import logger
from colorama import Fore, Style


class PineconeMemory(MemoryProviderSingleton):
    def __init__(self, cfg):
        pinecone_api_key = cfg.pinecone_api_key
        pinecone_region = cfg.pinecone_region
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_region)
        dimension = 1536
        metric = "cosine"
        pod_type = "p1"
        table_name = "auto-gpt"
        # this assumes we don't start with memory.
        # for now this works.
        # we'll need a more complicated and robust system if we want to start with memory.
        self.vec_num = 0

        try:
            pinecone.whoami()
        except Exception as e:
            logger.typewriter_log("FAILED TO CONNECT TO PINECONE", Fore.RED, Style.BRIGHT + str(e) + Style.RESET_ALL)
            logger.double_check("Please ensure you have setup and configured Pinecone properly for use. " +
                               f"You can check out {Fore.CYAN + Style.BRIGHT}https://github.com/Torantulino/Auto-GPT#-pinecone-api-key-setup{Style.RESET_ALL} to ensure you've set up everything correctly.")
            exit(1)

        if table_name not in pinecone.list_indexes():
            pinecone.create_index(table_name, dimension=dimension, metric=metric, pod_type=pod_type)
        self.index = pinecone.Index(table_name)

    def add(self, data):
        vector = get_ada_embedding(data)
        # no metadata here. We may wish to change that long term.
        resp = self.index.upsert([(str(self.vec_num), vector, {"raw_text": data})])
        _text = f"Inserting data into memory at index: {self.vec_num}:\n data: {data}"
        self.vec_num += 1
        return _text

    def get(self, data):
        return self.get_relevant(data, 1)

    def clear(self):
        self.index.delete(deleteAll=True)
        return "Obliviated"

    def get_relevant(self, data, num_relevant=5):
        """
        Returns all the data in the memory that is relevant to the given data.
        :param data: The data to compare to.
        :param num_relevant: The number of relevant data to return. Defaults to 5
        """
        query_embedding = get_ada_embedding(data)
        results = self.index.query(query_embedding, top_k=num_relevant, include_metadata=True)
        sorted_results = sorted(results.matches, key=lambda x: x.score)
        return [str(item['metadata']["raw_text"]) for item in sorted_results]

    def get_stats(self):
        return self.index.describe_index_stats()

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