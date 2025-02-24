
#!/bin/bash
# Create a virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Update pip to the latest version
pip install --upgrade pip

# Install the necessary packages from requirements.txt
pip install -r requirements.txt

echo "Setup complete. Virtual environment 'env' is ready to use."
