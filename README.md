# mle-project

Objective Develop and present a machine learning project that includes data preprocessing, model training, pipeline orchestration, containerization, and (as a bonus) API development and CI/CD pipeline suggestion.
This README includes:
- Project Setup
- Docker Setup
- 1. Dataset Selection & Model Training
- 2. Workflow Automation Tools
- 3. Containerization
- 4. CI/CD Proposal
- 5. Model Monitoring Strategies

## Project Setup
This repo includes the Dockerfile, EDA, data ingestion, data processing, model training, model evaluation, and airflow orchestration of the pipeline. Below is the pipeline set up:
![Logo](images/pipeline.jpeg)

Due to data size limitation on GitHub, please download the data folder provided via email and put the data folder under the root directory:
![Logo](images/datafolder.jpeg)

After following Docker Setup instructions #1-4 in the next section, the pipeline can be triggered by the following steps:
1. Go to http://localhost:8080
2. Use "airflow" as both username and password to log into airflow
3. Find ‘mlops_pipeline’ from the list, click the run button on the right
4. The pipeline should be triggered, wait for the entire process to finish
5. The results are stored in the /data folder
6. For clean up, refer to Docker Setup #5

## Docker Setup
1. Build docker image from dockerfile (image name: airflow_custom:latest). \
If using terminal, cd to the folder where the dockerfile is located and run: docker build -t airflow-custom:latest .\
If using Linux: echo -e "AIRFLOW_UID=$(id -u)" > .env

2. To create first user account, run: docker compose up airflow-init
3. To start all services, run: docker compose up
4. Please keep the terminal where docker compose up was executed in
5. To clean up, run: docker compose down --volumes --rmi all 


For terminal access after the docker containers are up, do the following:
6. For terminal access of the airflow container, run: ./airflow.sh bash
7. For the list of all dags, run: airflow dags list
8. For triggering the dag (dag_id should be mlops_pipeline), run: airflow dags trigger <dag_id>

##

