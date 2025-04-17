@echo off
echo Setting up Airflow...

REM Set environment variables
set AIRFLOW_HOME=%USERPROFILE%\airflow
set AIRFLOW_CONFIG=%AIRFLOW_HOME%\airflow.cfg

echo Creating Airflow directories...
if not exist "%AIRFLOW_HOME%" mkdir "%AIRFLOW_HOME%"
if not exist "%AIRFLOW_HOME%\dags" mkdir "%AIRFLOW_HOME%\dags"

echo Copying DAG file...
copy /Y "dags\lpr_to_neo4j_dag.py" "%AIRFLOW_HOME%\dags\" || (
    echo Failed to copy DAG file
    exit /b 1
)

echo Initializing Airflow database...
airflow db init || (
    echo Failed to initialize Airflow database
    exit /b 1
)

echo Creating Airflow admin user...
airflow users create ^
    --username admin ^
    --firstname Admin ^
    --lastname User ^
    --role Admin ^
    --email admin@example.com ^
    --password admin || (
    echo Failed to create admin user
    exit /b 1
)

echo Starting Airflow webserver...
start "Airflow Webserver" cmd /k "airflow webserver -p 8080"

echo Starting Airflow scheduler...
start "Airflow Scheduler" cmd /k "airflow scheduler"

echo.
echo Airflow setup complete!
echo Webserver URL: http://localhost:8080
echo Username: admin
echo Password: admin
echo.
