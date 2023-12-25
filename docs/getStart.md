# Getting Started with SimpleApp_Backend

Welcome to SimpleApp_Backend! This guide will help you set up and start using the application quickly and efficiently.

## Requirements

Before you begin, ensure that you have Python installed on your system. Our application is compatible with Python versions 3.8 through 3.11. If you don't have Python installed, please download it from [Python's official website](https://www.python.org/downloads/).

Along with Python, our application requires several additional packages:

- `uvicorn`
- `fastapi`
- `requests`
- `psutil`

These packages are necessary for the application to run properly, as they provide web server capabilities, API functionalities, network communication, and system monitoring tools.

## Installation

### Step 1: Install Required Packages

Once you have Python installed, you can easily install the required packages using Python’s package manager, pip. Open your command line interface (CLI) and type the following command:

```bash
pip install uvicorn fastapi psutil requests
```

This command tells pip to download and install the uvicorn, fastapi, psutil, and requests packages from the Python Package Index (PyPI).


### Step 2: Run the Application
Navigate to the directory where your main.py file is located. You can start the application by running the following command in your CLI:

```bash
python main.py
```
Note: The command might vary slightly based on your Python installation. For instance, if you have multiple versions of Python installed, you might need to use python3 instead of python.

### Troubleshooting
If you encounter any issues while setting up or running the application, here are a few common problems and solutions:

- Python or Pip Not Recognized: Ensure that Python and pip are correctly installed and that their paths are added to your system's environment variables.
- Package Installation Errors: Check your internet connection and make sure you have the necessary permissions to install packages.
- Application Doesn’t Start: Double-check the directory path and ensure that main.py is present and correctly named.



