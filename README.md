# mle-project

Objective Develop and present a machine learning project that includes data preprocessing, model training, pipeline orchestration, containerization, and (as a bonus) API development and CI/CD pipeline suggestion.

## Project Setup
This repo includes the Dockerfile, EDA, data ingestion, data processing, model training, model evaluation, and airflow orchestration of the pipeline. Below is the pipeline set up:
![Logo](images/pipeline.jpeg)

Due to data size limitation on GitHub, please download the data folder provided via email and put the data folder under the root directory:
![Logo](images/datafolder.jpeg)

After following Docker Setup instructions #1-4 in the next section, the pipeline can be triggered by the following steps:
- 1. Go to http://localhost:8080
- 2. Use "airflow" as both username and password to log into airflow
- 3. Find ‘mlops_pipeline’ from the list, click the run button on the right
- 4. The pipeline should be triggered, wait for the entire process to finish
- 5. The results are stored in the /data folder
- 6. For clean up, refer to Docker Setup #5
