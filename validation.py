#!/usr/bin/python3
import os
import json
import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)  # Initialize Colorama

# Function for JSON validation
def validate_json(data, file_path):
    try:
        json.loads(data)
        return None  # Return None for successful validation
    except ValueError as e:
        return f"Error in file '{file_path}': {str(e)}"

# Function for YAML validation
def validate_yaml(data, file_path):
    try:
        yaml.safe_load(data)
        return None  # Return None for successful validation
    except yaml.YAMLError as e:
        return f"Error in file '{file_path}': {str(e)}"

# Current directory
directory = os.environ.get('PWD')

# JSON Schema for JSON file validation (if needed)
json_schema = {
    "type": "object",
    "properties": {
        "example": {"type": "string"}
    },
    "required": ["example"]
}

# Create a list to store system errors
system_errors = []

# Recursively go through all files in the current directory and its subdirectories
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(('.yml', '.yaml', '.json')):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                data = f.read()
                error = None
                if file.endswith(('.json',)):
                    error = validate_json(data, file_path)
                elif file.endswith(('.yml', '.yaml')):
                    error = validate_yaml(data, file_path)
                if error:
                    system_errors.append(f"System error: {error}")

if system_errors:
    for error in system_errors:
        print(f"{Fore.RED}{error}")
        print(f"{Fore.MAGENTA}{'-'*40}")  # Horizontal line for separation
    sys.exit(1)
else:
    print(f"{Fore.GREEN}Validation successful.")
    sys.exit(0)
