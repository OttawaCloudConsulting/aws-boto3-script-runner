# AWS boto3 Script Runner
Dockerfile to build a dynamic AWS Boto3 Script

## Table of Contents

- [AWS boto3 Script Runner](#aws-boto3-script-runner)
- [Boto3 Script Execution Container](#boto3-script-execution-container)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
  - [Building the Docker Image](#building-the-docker-image)
  - [Running the Container](#running-the-container)
  - [Overriding CMD](#overriding-cmd)
  - [Environment Variables](#environment-variables)
  - [Volume Mounting](#volume-mounting)
  - [Example Usage](#example-usage)
    - [Running a Python Script](#running-a-python-script)
    - [Overriding the Default Command](#overriding-the-default-command)
    - [Listing Installed Packages](#listing-installed-packages)
    - [Debugging](#debugging)
  - [References](#references)

## Introduction

This repository provides a Docker setup for executing Python scripts that utilize the Boto3 library to interact with AWS services. The container is based on the official Python 3.10 image and includes Boto3 pre-installed. It is designed to run Python scripts specified at runtime, with dependencies managed through a requirements file.

Key features:

- Uses the `python:3.10` base image.
- Installs `boto3` for AWS service interactions.
- Dynamically installs Python dependencies from a specified requirements file.
- Executes a specified Python script at runtime.
- Supports passing environment variables for configuration.
- Allows overriding the default command for flexible script execution.

This container is particularly useful for CI/CD pipelines, automated testing, and any scenario where you need a consistent environment to run Python scripts that interact with AWS.

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- **Docker**: Install Docker from the [official website](https://www.docker.com/products/docker-desktop).

Additionally, you will need:

- A local directory containing your Python scripts and a `requirements.txt` file. The `requirements.txt` must be present, even if no dependencies are present to be installed.
- AWS credentials (API key, API secret, and API token) if your scripts require access to AWS services.

Example directory structure:

```bash
├── src
│   ├── list_s3_buckets.py
│   ├── list_ec2_instances.py
│   └── requirements.txt
```

Make sure the paths to your Python scripts and `requirements.txt` file are correct when running the container.

## Building the Docker Image

To build the Docker image, follow these steps:

1. **Clone the Repository**: If you haven't already, clone this repository to your local machine.

```bash
git clone <repository-url>
cd <repository-directory>
```

2. **Create the `entrypoint-python.sh` Script**: Ensure that the `entrypoint-python.sh` script is present in the repository directory with the following content:

```bash
#!/bin/bash

# Ensure the necessary environment variables are set
if [ -z "$PYTHON_FILE" ] || [ -z "$REQUIREMENTS_FILE" ]; then
  echo "Error: PYTHON_FILE and REQUIREMENTS_FILE environment variables must be set."
  exit 1
fi

# Install dependencies from the specified requirements file
pip install -r "$REQUIREMENTS_FILE"

# Execute the specified Python file
python "$PYTHON_FILE"
```

3. **Build the Docker Image**: Run the following command to build the Docker image. Make sure you are in the directory containing the Dockerfile and `entrypoint-python.sh`.

```bash
docker build -t my-python-boto3-container .
```

This command will create a Docker image named `my-python-boto3-container` based on the `python:3.10` image, with `boto3` installed, and an entrypoint script set up to handle dependency installation and script execution.

You can verify that the image has been created by listing your Docker images:

```bash
docker images
```

You should see `my-python-boto3-container` listed among the available images.

## Running the Container

To run the container, you need to mount your local directory containing the Python scripts and requirements file into the container and pass the necessary environment variables. Follow these steps:

1. **Prepare Your Local Directory**: Ensure that your Python scripts and `requirements.txt` file are in a directory, for example, `./src`.

2. **Run the Container**: Use the following command to run the container. Replace the placeholders with your actual paths and values:

```bash
docker run --rm -v $(pwd)/src:/app \
  -e PYTHON_FILE=/app/list_s3_buckets.py \
  -e REQUIREMENTS_FILE=/app/requirements.txt \
  -e API_KEY=your_api_key \
  -e API_SECRET=your_api_secret \
  -e API_TOKEN=your_api_token \
  my-python-boto3-container
```

- `-v $(pwd)/src:/app`: Mounts the local `src` directory to `/app` in the container.
- `-e PYTHON_FILE=/app/list_s3_buckets.py`: Sets the environment variable `PYTHON_FILE` to the path of the Python script inside the container.
- `-e REQUIREMENTS_FILE=/app/requirements.txt`: Sets the environment variable `REQUIREMENTS_FILE` to the path of the requirements file inside the container.
- `-e API_KEY=your_api_key`: Sets the environment variable `API_KEY` for your AWS API key.
- `-e API_SECRET=your_api_secret`: Sets the environment variable `API_SECRET` for your AWS API secret.
- `-e API_TOKEN=your_api_token`: Sets the environment variable `API_TOKEN` for your AWS API token.

This command will start the container, install the dependencies specified in `requirements.txt`, and execute the Python script specified by `PYTHON_FILE`.

3. **Verify Execution**: Ensure that the script runs as expected. Check the output logs for any errors or confirmation that the script executed successfully.

The `--rm` flag ensures that the container is removed after it exits, keeping your environment clean.

## Overriding CMD

The Dockerfile is set up with a default `CMD` that runs the `entrypoint-python.sh` script. However, you can override this default command when you run the container. This can be useful if you want to execute a different script or command without modifying the Dockerfile or rebuilding the image.

To override the `CMD`, simply provide the new command at the end of the `docker run` command. Here’s an example:

```bash
docker run --rm -v $(pwd)/src:/app \
  -e API_KEY=your_api_key \
  -e API_SECRET=your_api_secret \
  -e API_TOKEN=your_api_token \
  my-python-boto3-container \
  python /app/list_ec2_instances.py
```

In this example, the container will execute `python /app/list_ec2_instances.py` instead of the default `CMD` specified in the Dockerfile.

Another example is running a bash command:

```bash
docker run --rm -v $(pwd)/src:/app \
  -e API_KEY=your_api_key \
  -e API_SECRET=your_api_secret \
  -e API_TOKEN=your_api_token \
  my-python-boto3-container \
  /bin/bash -c "pip list"
```

This command will start a Bash bash in the container and list all installed Python packages.

Overriding the `CMD` is useful for debugging, running different scripts, or performing other operations without changing the container’s configuration.


## Environment Variables

The container relies on several environment variables to configure its behavior. These variables are used to specify the paths of the Python script and the requirements file, as well as AWS credentials. Below is a description of each environment variable:

- `PYTHON_FILE`: The path to the Python script you want to execute inside the container. This path should be relative to the mounted directory.
- `REQUIREMENTS_FILE`: The path to the `requirements.txt` file inside the container. This file contains the dependencies that need to be installed before executing the Python script.
- `API_KEY`: Your AWS API key. This is required if your Python script needs to interact with AWS services using Boto3.
- `API_SECRET`: Your AWS API secret. This is required if your Python script needs to interact with AWS services using Boto3.
- `API_TOKEN`: Your AWS API token. This is required if your Python script needs to interact with AWS services using Boto3.

Example of setting environment variables when running the container:

```bash
docker run --rm -v $(pwd)/src:/app \
  -e PYTHON_FILE=/app/list_s3_buckets.py \
  -e REQUIREMENTS_FILE=/app/requirements.txt \
  -e API_KEY=your_api_key \
  -e API_SECRET=your_api_secret \
  -e API_TOKEN=your_api_token \
  my-python-boto3-container
```

Make sure to replace the placeholder values (`your_api_key`, `your_api_secret`, `your_api_token`) with your actual AWS credentials.

These environment variables ensure that the container has all the necessary information to install dependencies and run the specified Python script, as well as access AWS services securely.

## Volume Mounting

To run the container with the necessary scripts and requirements file, you must mount your local directory into the container. This ensures that the container has access to these files at runtime. Volume mounting is done using the `-v` flag in the `docker run` command.

Here’s how to properly mount your local directory:

```bash
docker run --rm -v $(pwd)/src:/app \
  -e PYTHON_FILE=/app/list_s3_buckets.py \
  -e REQUIREMENTS_FILE=/app/requirements.txt \
  -e API_KEY=your_api_key \
  -e API_SECRET=your_api_secret \
  -e API_TOKEN=your_api_token \
  my-python-boto3-container
```

In this command:

- `-v $(pwd)/src:/app`: Mounts the `src` directory from your current working directory (`$(pwd)`) to `/app` in the container.

The mounted directory `/app` inside the container will contain the Python scripts and `requirements.txt` file. This allows the container to access and execute these files as if they were part of the container’s filesystem.

**Important Notes**:

- Ensure the local directory (`src`) contains the Python scripts and `requirements.txt` file.
- The paths provided in the environment variables (`PYTHON_FILE` and `REQUIREMENTS_FILE`) should match the mounted paths inside the container.
- Changes to the scripts or `requirements.txt` file in the local directory are immediately reflected in the container, as the directory is mounted at runtime.

Example directory structure:

```
├── src
│   ├── list_s3_buckets.py
│   ├── list_ec2_instances.py
│   └── requirements.txt
```

This setup allows for flexibility and ensures that your container always uses the latest version of your scripts and dependencies without needing to rebuild the Docker image.

## Example Usage

Here are some example commands to illustrate how to use the Docker container for different scenarios:

### Running a Python Script

To run a specific Python script with its dependencies:

```bash
docker run --rm -v $(pwd)/src:/app \
  -e PYTHON_FILE=/app/list_s3_buckets.py \
  -e REQUIREMENTS_FILE=/app/requirements.txt \
  -e API_KEY=your_api_key \
  -e API_SECRET=your_api_secret \
  -e API_TOKEN=your_api_token \
  my-python-boto3-container
```

This command mounts the local `src` directory to `/app` in the container, sets the required environment variables, and runs the `list_s3_buckets.py` script.

### Overriding the Default Command

If you need to run a different Python script or perform a different action, you can override the default command:

```bash
docker run --rm -v $(pwd)/src:/app \
  -e API_KEY=your_api_key \
  -e API_SECRET=your_api_secret \
  -e API_TOKEN=your_api_token \
  my-python-boto3-container \
  python /app/list_ec2_instances.py
```

This command will execute the `list_ec2_instances.py` script instead of the default entrypoint.

### Listing Installed Packages

You can also use the container to run other commands, such as listing installed Python packages:

```bash
docker run --rm -v $(pwd)/src:/app \
  -e API_KEY=your_api_key \
  -e API_SECRET=your_api_secret \
  -e API_TOKEN=your_api_token \
  my-python-boto3-container \
  /bin/bash -c "pip list"
```

This command opens a Bash bash in the container and lists all installed Python packages.

### Debugging

For debugging purposes, you can start an interactive Bash session in the container:

```bash
docker run --rm -it -v $(pwd)/src:/app \
  -e API_KEY=your_api_key \
  -e API_SECRET=your_api_secret \
  -e API_TOKEN=your_api_token \
  my-python-boto3-container \
  /bin/bash
```

This command provides an interactive terminal where you can manually execute commands, inspect the file system, or troubleshoot issues.

## References

[AWS BOTO3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html#)

[Python 3.10 Documentation](https://www.python.org/downloads/release/python-3100/)

[Docker Documentation](https://docs.docker.com/)
 
[Docker Volume Mounts](https://docs.docker.com/storage/volumes/)
 
[Docker CMD vs ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact)
 
[Docker Environment Variables](https://docs.docker.com/compose/environment-variables/)
 
[bash Scripting Guide](https://www.bashscript.sh/)
