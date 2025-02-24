
import docker
import os
import subprocess

WORKSPACE_FOLDER = "auto_gpt_workspace"

def execute_python_file(file):
    """Execute a Python file in a Docker container and return the output"""

    print(f"Executing file '{file}' in workspace '{WORKSPACE_FOLDER}'")

    if not file.endswith(".py"):
        return "Error: Invalid file type. Only .py files are allowed."

    file_path = os.path.join(WORKSPACE_FOLDER, file)

    if not os.path.isfile(file_path):
        return f"Error: File '{file}' does not exist."

    try:
        client = docker.from_env()

        image_name = 'python:3.10'
        try:
            client.images.get(image_name)
            print(f"Image '{image_name}' found locally")
        except docker.errors.ImageNotFound:
            print(f"Image '{image_name}' not found locally, pulling from Docker Hub")
            # Use the low-level API to stream the pull response
            low_level_client = docker.APIClient()
            for line in low_level_client.pull(image_name, stream=True, decode=True):
                # Print the status and progress, if available
                status = line.get('status')
                progress = line.get('progress')
                if status and progress:
                    print(f"{status}: {progress}")
                elif status:
                    print(status)

        # Checking for Docker daemon availability
        try:
            client.ping()
        except docker.errors.APIError:
            return "Error: Docker daemon is not running. Please ensure Docker is running and try again."

        # Running the container
        container = client.containers.run(
            image_name,
            f'python {file}',
            volumes={
                os.path.abspath(WORKSPACE_FOLDER): {
                    'bind': '/workspace',
                    'mode': 'ro'}},
            working_dir='/workspace',
            stderr=True,
            stdout=True,
            detach=True,
        )

        output = container.wait()
        logs = container.logs().decode('utf-8')
        container.remove()

        return logs

    except Exception as e:
        return f"Error: {str(e)}"

def execute_shell(command_line):
    current_dir = os.getcwd()

    if not WORKSPACE_FOLDER in current_dir:  # Change dir into workspace if necessary
        work_dir = os.path.join(os.getcwd(), WORKSPACE_FOLDER)
        os.chdir(work_dir)

    print(f"Executing command '{command_line}' in working directory '{os.getcwd()}'")

    result = subprocess.run(command_line, capture_output=True, shell=True)
    output = f"STDOUT:\n{result.stdout.decode()}\nSTDERR:\n{result.stderr.decode()}"

    # Change back to whatever the prior working dir was
    os.chdir(current_dir)

    return output

# Specific modifications for improved Docker integration and error handling
# Specific modifications for improved JSON handling and command execution
# Specific modifications for improved file operations
# Specific modifications for improved operations
