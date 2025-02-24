"""Redis memory provider."""
from typing import Any, List, Optional
import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import numpy as np

from memory.base import MemoryProviderSingleton, get_ada_embedding
from logger import logger
from colorama import Fore, Style


SCHEMA = [
    TextField("data"),
    VectorField(
        "embedding",
        "HNSW",
        {
            "TYPE": "FLOAT32",
            "DIM": 1536,
            "DISTANCE_METRIC": "COSINE"
        }
    ),
]


class RedisMemory(MemoryProviderSingleton):
    def __init__(self, cfg):
        """
        Initializes the Redis memory provider.

        Args:
            cfg: The config object.

        Returns: None
        """
        redis_host = cfg.redis_host
        redis_port = cfg.redis_port
        redis_password = cfg.redis_password
        self.dimension = 1536
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=0  # Cannot be changed
        )
        self.cfg = cfg

        # Check redis connection
        try:
            self.redis.ping()
        except redis.ConnectionError as e:
            logger.typewriter_log("FAILED TO CONNECT TO REDIS", Fore.RED, Style.BRIGHT + str(e) + Style.RESET_ALL)
            logger.double_check("Please ensure you have setup and configured Redis properly for use. " +
                                f"You can check out {Fore.CYAN + Style.BRIGHT}https://github.com/Torantulino/Auto-GPT#redis-setup{Style.RESET_ALL} to ensure you've set up everything correctly.")
            exit(1)

        if cfg.wipe_redis_on_start:
            self.redis.flushall()
        try:
            self.redis.ft(f"{cfg.memory_index}").create_index(
                fields=SCHEMA,
                definition=IndexDefinition(
                    prefix=[f"{cfg.memory_index}:"],
                    index_type=IndexType.HASH
                    )
                )
        except Exception as e:
            print("Error creating Redis search index: ", e)
        existing_vec_num = self.redis.get(f'{cfg.memory_index}-vec_num')
        self.vec_num = int(existing_vec_num.decode('utf-8')) if\
            existing_vec_num else 0

    def add(self, data: str) -> str:
        """
        Adds a data point to the memory.

        Args:
            data: The data to add.

        Returns: Message indicating that the data has been added.
        """
        if 'Command Error:' in data:
            return ""
        vector = get_ada_embedding(data)
        vector = np.array(vector).astype(np.float32).tobytes()
        data_dict = {
            b"data": data,
            "embedding": vector
        }
        pipe = self.redis.pipeline()
        pipe.hset(f"{self.cfg.memory_index}:{self.vec_num}", mapping=data_dict)
        _text = f"Inserting data into memory at index: {self.vec_num}:\n"\
            f"data: {data}"
        self.vec_num += 1
        pipe.set(f'{self.cfg.memory_index}-vec_num', self.vec_num)
        pipe.execute()
        return _text

    def get(self, data: str) -> Optional[List[Any]]:
        """
        Gets the data from the memory that is most relevant to the given data.

        Args:
            data: The data to compare to.

        Returns: The most relevant data.
        """
        return self.get_relevant(data, 1)

    def clear(self) -> str:
        """
        Clears the redis server.

        Returns: A message indicating that the memory has been cleared.
        """
        self.redis.flushall()
        return "Obliviated"

    def get_relevant(
        self,
        data: str,
        num_relevant: int = 5
    ) -> Optional[List[Any]]:
        """
        Returns all the data in the memory that is relevant to the given data.
        Args:
            data: The data to compare to.
            num_relevant: The number of relevant data to return.

        Returns: A list of the most relevant data.
        """
        query_embedding = get_ada_embedding(data)
        base_query = f"*=>[KNN {num_relevant} @embedding $vector AS vector_score]"
        query = Query(base_query).return_fields(
            "data",
            "vector_score"
        ).sort_by("vector_score").dialect(2)
        query_vector = np.array(query_embedding).astype(np.float32).tobytes()

        try:
            results = self.redis.ft(f"{self.cfg.memory_index}").search(
                query, query_params={"vector": query_vector}
            )
        except Exception as e:
            print("Error calling Redis search: ", e)
            return None
        return [result.data for result in results.docs]

    def get_stats(self):
        """
        Returns: The stats of the memory index.
        """
        return self.redis.ft(f"{self.cfg.memory_index}").info()


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