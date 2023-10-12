# Physio Backend

This section of the repository is devoted to processing user input. It handles user interaction through various features including API integration, database interaction, virtual environments, and workflow automation.

## Setting Up Environment Variables

To operate this module, you'll need access to the OpenAI Models API. You should provide your API key in a `.env` file. Use the template below to create your `.env` file. Please replace the placeholders with your actual data:

```sh
AZURE_OPENAI_KEY=<your_azure_openai_key>
AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>
AZURE_ENGINE_NAME=<your_azure_engine_name>

AIRFLOW_UID=<airflow_uid>
AIRFLOW_GID=<airflow_gid>

MONGO_USER=<mongo_user>
MONGO_PASSWORD=<mongo_password>
```

## Creating a Virtual Environment

Setting up a virtual environment is crucial for isolating the dependencies required by this module. Use the following steps:

```sh
virtualenv venv --python=python3.10
source venv/bin/activate
pip install -r requirements.txt
pip install -e backend
```
