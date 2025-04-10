import logging
import os
import random
import re
import time
from logging import LogRecord
from colorama import Fore

from colorama import Style

import speak
from config import Config
from config import Singleton

cfg = Config()

'''
Logger that handle titles in different colors.
Outputs logs in console, activity.log, and errors.log
For console handler: simulates typing
'''


class Logger(metaclass=Singleton):
    def __init__(self):
        # create log directory if it doesn't exist
        log_dir = os.path.join('..', 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = "activity.log"
        error_file = "error.log"

        console_formatter = AutoGptFormatter('%(title_color)s %(message)s')

        # Create a handler for console which simulate typing
        self.typing_console_handler = TypingConsoleHandler()
        self.typing_console_handler.setLevel(logging.INFO)
        self.typing_console_handler.setFormatter(console_formatter)

        # Create a handler for console without typing simulation
        self.console_handler = ConsoleHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(console_formatter)

        # Info handler in activity.log
        self.file_handler = logging.FileHandler(os.path.join(log_dir, log_file))
        self.file_handler.setLevel(logging.DEBUG)
        info_formatter = AutoGptFormatter('%(asctime)s %(levelname)s %(title)s %(message_no_color)s')
        self.file_handler.setFormatter(info_formatter)

        # Error handler error.log
        error_handler = logging.FileHandler(os.path.join(log_dir, error_file))
        error_handler.setLevel(logging.ERROR)
        error_formatter = AutoGptFormatter(
            '%(asctime)s %(levelname)s %(module)s:%(funcName)s:%(lineno)d %(title)s %(message_no_color)s')
        error_handler.setFormatter(error_formatter)

        self.typing_logger = logging.getLogger('TYPER')
        self.typing_logger.addHandler(self.typing_console_handler)
        self.typing_logger.addHandler(self.file_handler)
        self.typing_logger.addHandler(error_handler)
        self.typing_logger.setLevel(logging.DEBUG)

        self.logger = logging.getLogger('LOGGER')
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(error_handler)
        self.logger.setLevel(logging.DEBUG)

    def typewriter_log(
            self,
            title='',
            title_color='',
            content='',
            speak_text=False,
            level=logging.INFO):
        if speak_text and cfg.speak_mode:
            speak.say_text(f"{title}. {content}")

        if content:
            if isinstance(content, list):
                content = " ".join(content)
        else:
            content = ""

        self.typing_logger.log(level, content, extra={'title': title, 'color': title_color})

    def debug(
            self,
            message,
            title='',
            title_color='',
    ):
        self._log(title, title_color, message, logging.DEBUG)

    def warn(
            self,
            message,
            title='',
            title_color='',
    ):
        self._log(title, title_color, message, logging.WARN)

    def error(
            self,
            title,
            message=''
    ):
        self._log(title, Fore.RED, message, logging.ERROR)

    def _log(
            self,
            title='',
            title_color='',
            message='',
            level=logging.INFO):
        if message:
            if isinstance(message, list):
                message = " ".join(message)
        self.logger.log(level, message, extra={'title': title, 'color': title_color})

    def set_level(self, level):
        self.logger.setLevel(level)
        self.typing_logger.setLevel(level)

    def double_check(self, additionalText=None):
        if not additionalText:
            additionalText = "Please ensure you've setup and configured everything correctly. Read https://github.com/Torantulino/Auto-GPT#readme to double check. You can also create a github issue or join the discord and ask there!"

        self.typewriter_log("DOUBLE CHECK CONFIGURATION", Fore.YELLOW, additionalText)


'''
Output stream to console using simulated typing
'''


class TypingConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        min_typing_speed = 0.05
        max_typing_speed = 0.01

        msg = self.format(record)
        try:
            words = msg.split()
            for i, word in enumerate(words):
                print(word, end="", flush=True)
                if i < len(words) - 1:
                    print(" ", end="", flush=True)
                typing_speed = random.uniform(min_typing_speed, max_typing_speed)
                time.sleep(typing_speed)
                # type faster after each word
                min_typing_speed = min_typing_speed * 0.95
                max_typing_speed = max_typing_speed * 0.95
            print()
        except Exception:
            self.handleError(record)


class ConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        msg = self.format(record)
        try:
            print(msg)
        except Exception:
            self.handleError(record)


class AutoGptFormatter(logging.Formatter):
    """
    Allows to handle custom placeholders 'title_color' and 'message_no_color'.
    To use this formatter, make sure to pass 'color', 'title' as log extras.
    """
    def format(self, record: LogRecord) -> str:
        if (hasattr(record, 'color')):
            record.title_color = getattr(record, 'color') + getattr(record, 'title') + " " + Style.RESET_ALL
        else:
            record.title_color = getattr(record, 'title')
        if hasattr(record, 'msg'):
            record.message_no_color = remove_color_codes(getattr(record, 'msg'))
        else:
            record.message_no_color = ''
        return super().format(record)


def remove_color_codes(s: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', s)


logger = Logger()

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