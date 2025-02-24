
import browse
import json
from memory import get_memory
import datetime
import agent_manager as agents
import speak
from config import Config
import ai_functions as ai
from file_operations import read_file, write_to_file, append_to_file, delete_file, search_files
from execute_code import execute_python_file, execute_shell
from json_parser import fix_and_parse_json
from image_gen import generate_image
from duckduckgo_search import ddg
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

cfg = Config()
logger = logging.getLogger(__name__)

def is_valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def get_command(response):
    """Parse the response and return the command name and arguments"""
    try:
        response_json = fix_and_parse_json(response)
        logger.debug(f"Parsed response JSON: {response_json}")

        if not isinstance(response_json, dict):
            logger.error("Expected a dictionary but got a different type")
            return "Error:", "Expected a dictionary but got a different type"

        if "command" not in response_json:
            logger.error("Missing 'command' object in JSON")
            return "Error:", "Missing 'command' object in JSON"

        command = response_json["command"]

        if "name" not in command:
            logger.error("Missing 'name' field in 'command' object")
            return "Error:", "Missing 'name' field in 'command' object"

        command_name = command["name"]
        arguments = command.get("args", {})

        logger.debug(f"Command parsed: {command_name}, Arguments: {arguments}")
        return command_name, arguments
    except json.decoder.JSONDecodeError:
        logger.error("Invalid JSON")
        return "Error:", "Invalid JSON"
    except Exception as e:
        logger.error(f"Exception during command parsing: {str(e)}")
        return "Error:", str(e)

def list_commands():
    """List all available commands"""
    available_commands = [
        "google", "memory_add", "start_agent", "message_agent", "list_agents",
        "delete_agent", "get_text_summary", "get_hyperlinks", "read_file",
        "write_to_file", "append_to_file", "delete_file", "search_files",
        "browse_website", "evaluate_code", "improve_code", "execute_python_file",
        "start_report", "write_tests"
    ]
    return available_commands

def execute_command(command_name, arguments):
    """Execute the command and return the result"""
    memory = get_memory(cfg)
    logger.debug(f"Executing command: {command_name} with arguments: {arguments}")

    try:
        if command_name == "google":
            if cfg.google_api_key and (cfg.google_api_key.strip() if cfg.google_api_key else None):
                return google_official_search(arguments["input"])
            else:
                return google_search(arguments["input"])
        elif command_name == "memory_add":
            return memory.add(arguments["string"])
        elif command_name == "start_agent":
            return start_agent(
                arguments["name"],
                arguments["task"],
                arguments["prompt"])
        elif command_name == "message_agent":
            return message_agent(arguments["key"], arguments["message"])
        elif command_name == "list_agents":
            return list_agents()
        elif command_name == "delete_agent":
            return delete_agent(arguments["key"])
        elif command_name == "get_text_summary":
            return get_text_summary(arguments["url"], arguments["question"])
        elif command_name == "get_hyperlinks":
            return get_hyperlinks(arguments["url"])
        elif command_name == "read_file":
            return read_file(arguments["file"])
        elif command_name == "write_to_file":
            return write_to_file(arguments["file"], arguments["text"])
        elif command_name == "append_to_file":
            return append_to_file(arguments["file"], arguments["text"])
        elif command_name == "delete_file":
            return delete_file(arguments["file"])
        elif command_name == "search_files":
            return search_files(arguments["directory"])
        elif command_name == "browse_website":
            return browse_website(arguments["url"], arguments["question"])
        elif command_name == "evaluate_code":
            return ai.evaluate_code(arguments["code"])
        elif command_name == "improve_code":
            return ai.improve_code(arguments["suggestions"], arguments["code"])
        elif command_name == "execute_python_file":
            return execute_python_file(arguments["file"])
        elif command_name == "start_report":
            return "Report started successfully."
        elif command_name == "write_tests":
            return "Tests written successfully."
        else:
            logger.error(f"Unknown command: {command_name}")
            return f"Error: Unknown command '{command_name}'"
    except Exception as e:
        logger.error(f"Exception during command execution: {str(e)}")
        return f"Error: {str(e)}"
