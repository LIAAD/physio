
## Running Airflow

To establish an environment for Airflow and initialize the required directories, use these commands:

```sh
mkdir logs plugins
docker-compose up
```

If you want to test Airflow, run the following command:

```sh
docker exec airflow-worker airflow dags test pipeline --conf '{"chat": {"last_question": "I feel pain on my lower back. What can I do?", "history": []}}'
```

The Airflow webserver is accessible at [localhost:8080](http://localhost:8080/). Use these credentials to log in:

* Username: airflow
* Password: airflow

You can trigger a workflow run using the REST API:

```sh
curl \
  -u airflow:airflow \
  -X POST \
  -H "Content-type: application/json"  \
  -d '{"chat": [{"question": "I feel pain on my lower back. What can I do?", "answer": ""}]}' 
  'http://localhost:8080/api/v1/dags/pipeline/dagRuns'
```

To check the status of your run, use the following command:

```sh
curl \
  -u airflow:airflow \
  -X GET \
  -H "Content-type: application/json" \
  -d '{"chat": [{"question": "I feel pain on my lower back. What can I do?", "answer": ""}]}' 
  'https://airflow.apache.org/api/v1/dags/pipeline/dagRuns/{dag_run_id}'
```

Please replace `{dag_run_id}` with the actual ID of your workflow run.