# Airflow Docker Learning Project

Welcome! This project is designed specifically for beginners to learn how to run [Apache Airflow](https://airflow.apache.org/) locally using [Docker](https://www.docker.com/).

It favors simple, reliable setups over complex, production-ready architectures. This means no Kubernetes, Celery, or Redis. Just pure, simple Airflow running on your computer.

---

## 📖 Concepts Explained Simply

Before we run commands, let's understand the core tools we are using.

### Docker Concepts

*   **What is Docker?** Docker is a tool that allows you to package software and all its dependencies (like Python, specific libraries, or system tools) into a standardized unit for software development. This solves the "it works on my machine" problem.
*   **What is a Docker Image?** Think of an image as a blueprint or a recipe. It contains a snapshot of an operating system, software, and configuration. In our project, our `Dockerfile` is the recipe that builds our specific Airflow image.
*   **What is a Docker Container?** If an image is the blueprint, a container is the actual house built from that blueprint. It is a running instance of an image. You can have multiple containers running from the same image.
*   **What does Docker Compose do?** Modern applications rarely run in a single container. You usually need a web server, a database, maybe a queue. Docker Compose is a tool that lets you define and run multi-container Docker applications using a single YAML file (`docker-compose.yaml`). One command (`docker compose up`) brings everything up together.

### Airflow Concepts

*   **What is Airflow?** Airflow is an open-source platform used to author, schedule, and monitor workflows. It's often used in Data Engineering to orchestrate ETL (Extract, Transform, Load) pipelines.
*   **Why does Airflow need multiple services?** Airflow isn't just one program; it's a distributed system. It needs:
    1.  A place to store information about tasks (Database).
    2.  A program to decide when tasks should run (Scheduler).
    3.  A user interface so you can see what's happening (Web UI).
    Docker Compose easily manages these separate pieces.
*   **What is a DAG?** DAG stands for Directed Acyclic Graph. In Airflow, a DAG is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies. It's basically the script that defines your workflow.
*   **What is a Task?** A task is a single unit of work in your DAG. For example, downloading a file is a task, transforming data is another task.
*   **What does a Scheduler do?** The Scheduler is the heart of Airflow. It constantly reads your DAG files, checks if the schedule dictates a task should run, and if so, sends that task to an Executor to run it.
*   **What does the Airflow Web UI do?** The Web UI is a dashboard accessed via your browser. It lets you visually inspect your DAGs, see if tasks succeeded or failed, read logs to debug issues, and manually start runs.
*   **What does the metadata database do?** The database keeps track of everything. It stores the definitions of your DAGs, the history of task executions (success/failure times), and user credentials.
*   **Why Postgres?** We use PostgreSQL because it is the recommended and most reliable database backend for Airflow. While Airflow *can* use SQLite for extreme simplicity, it lacks features and can cause issues even in learning environments. Postgres is robust and standard.

---

## 📂 Project Structure

Here is what each file and folder does:

*   `docker-compose.yaml`: The master configuration file. It tells Docker Compose what containers to start, how they talk to each other, and what folders to share.
*   `Dockerfile`: The blueprint for our custom Airflow container. We use it so we can install custom Python packages.
*   `requirements.txt`: A list of Python packages our DAGs need (e.g., `pandas`). The `Dockerfile` reads this.
*   `.env.example`: A template file. Docker Compose uses a hidden `.env` file to read variables. You will copy this file to create your `.env`.
*   `dags/`: This is where Airflow looks for your DAG files (Python scripts). We share this folder with the container so you can edit DAGs locally and see changes instantly.
    *   `hello_airflow_dag.py`: Our sample beginner pipeline.
*   `data/`: A folder we use to simulate reading and writing local data files.
*   `logs/`: Where Airflow writes task execution logs. Useful for debugging without using the Web UI.
*   `plugins/`: (Empty for now) Where you would put custom Airflow operators or UI plugins.
*   `scripts/`: Useful bash scripts, like `smoke_test.sh` to check if the server is healthy.

---

## 🐳 Understanding `docker-compose.yaml`

If you open `docker-compose.yaml`, you will see several `services` defined. Here is what happens when you run `docker compose up`:

1.  **`postgres`**: Docker starts a database container.
2.  **`airflow-init`**: This container starts, waits for Postgres to be ready, then sets up the Airflow database tables and creates your admin user. Then it gracefully exits.
3.  **`airflow-scheduler`**: Once `airflow-init` is done, the scheduler starts continuously scanning the `dags/` folder.
4.  **`airflow-webserver`**: The web UI starts up and listens on port 8080.

**Local Volumes**: Notice the `volumes:` section under `x-airflow-common`. It looks like `./dags:/opt/airflow/dags`. This maps the `dags` folder on your computer (the left side) to the `/opt/airflow/dags` folder inside the running container (the right side). If you edit a file on your computer, the container instantly sees the change.

---

## 🐍 How the Sample DAG Works

Open `dags/hello_airflow_dag.py`. Read the comments carefully.

1.  **Imports**: We import Airflow tools and `pandas`.
2.  **Functions**: We define three plain Python functions (`extract_data`, `transform_data`, `load_data`). These functions read and write CSV files to the `/opt/airflow/data/...` paths. Remember, because of Docker volumes, these files appear in your local `data/` folder!
3.  **DAG Definition**: We use `with DAG(...) as dag:` to declare our pipeline, giving it a name (`hello_airflow_dag`), an owner, and telling it to run daily.
4.  **Operators**: We create `PythonOperator` instances. These tell Airflow "When this task runs, execute this specific Python function."
5.  **Dependencies**: `task_extract >> task_transform >> task_load` tells Airflow the exact order things must happen.

---

## 🚀 Getting Started Guide

Follow these steps exactly to run the project.

### 1. Prerequisites

You must have Docker installed on your computer.
*   **Windows/Mac**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
*   Ensure Docker Desktop is running (you should see the whale icon in your taskbar/menu bar).

### 2. Setup Configuration

Open your terminal or command prompt. Navigate to this project folder (`airflow-docker-learning`).

First, create your hidden environment file by copying the example:

**On Mac/Linux:**
```bash
cp .env.example .env
```

**On Windows:**
```cmd
copy .env.example .env
```

*Note: The `.env` file contains your user ID and default Airflow UI passwords (airflow / airflow).*

### 3. Build and Initialize

Because we added a custom `requirements.txt` (with `pandas`), we need to build our custom Docker image.

```bash
# This builds the image based on our Dockerfile
docker compose build
```

Now, initialize the database. This runs the `airflow-init` service once to set up the tables.

```bash
docker compose up airflow-init
```
*(Wait until it finishes. It should print a message saying it completed successfully or exit with code 0).*

### 4. Start Airflow

Start the remaining services in the background (`-d` means detached mode).

```bash
docker compose up -d
```

### 5. Log into the UI

1.  Open your web browser.
2.  Go to: **http://localhost:8080**
3.  Log in with:
    *   **Username**: `airflow`
    *   **Password**: `airflow`

### 6. Run the Sample DAG

1.  In the Airflow UI, find `hello_airflow_dag` in the list.
2.  On the far left, click the toggle switch to "Unpause" the DAG (it turns blue).
3.  On the far right, click the "Play" (▶) button and select **"Trigger DAG"**.
4.  Click on the name `hello_airflow_dag` to view its details.
5.  Go to the **Graph** view. You will see the boxes (`extract_data`, etc.) light up dark green as they run and finish successfully.
6.  Look inside your local computer's `airflow-docker-learning/data/processed` folder. You will see a `clean_data.csv` file created by Airflow!

### 7. Inspecting Logs

If a task fails (turns red), you need to know why.
1. In the Graph view, click on the failed task box.
2. Click the **"Log"** button at the top.
3. Read the text to find the Python error.

You can also view container logs in your terminal:
```bash
# View logs for the webserver
docker compose logs airflow-webserver
```

### 8. Adding a New DAG

Simply create a new `.py` file inside the `dags/` folder. Wait 30-60 seconds, and it will magically appear in the Airflow UI.

### 9. Installing a New Python Package

If you need a library like `requests`:
1. Open `requirements.txt`.
2. Add `requests==2.31.0` on a new line.
3. Rebuild the image: `docker compose build`
4. Restart the containers: `docker compose down` then `docker compose up -d`.

### 10. Stopping and Cleaning Up

When you are done for the day, stop the containers. Your data is safe.

```bash
docker compose stop
```

**To completely wipe everything and start fresh** (This deletes your database history!):

```bash
docker compose down --volumes --rmi all
```

---

## 🛠️ Beginner Troubleshooting

*   **Error: "port is already allocated"**: Something else on your computer is using port 8080 (maybe another web server). You can change `"8080:8080"` to `"8081:8080"` in the `docker-compose.yaml` under `airflow-webserver`, then go to `localhost:8081`.
*   **Containers keep restarting / Database errors**: Ensure you ran `docker compose up airflow-init` successfully before running `docker compose up -d`.
*   **DAG isn't showing up**: It takes the scheduler about 30-60 seconds to scan the `dags/` folder. Be patient. Check the top of the UI for import errors (red banners).
*   **Permission Denied errors writing to `data/`**: Ensure your `.env` file has the correct `AIRFLOW_UID`. On Linux, this must match your user ID (`id -u`). On Windows/Mac, 50000 usually works fine.

---

## 🏋️ Next Steps (Exercises for you)

1.  **Modify the Transform**: Open `dags/hello_airflow_dag.py`. Change the logic in `transform_data` to multiply the age by 2 instead of adding 5. Save the file, run the DAG again, and inspect the resulting CSV file.
2.  **Add a Task**: Add a fourth task at the end called `cleanup_task` that uses Python's `os` module to delete the `raw/dummy_data.csv` file after the pipeline is finished.
3.  **Break it on purpose**: Cause a syntax error in your DAG file on purpose. Look at the Airflow UI to see the bright red "Import Error" banner, which is how Airflow tells you your code is broken.
4.  **Use a BashOperator**: Import `BashOperator` from `airflow.operators.bash` and create a task that runs `echo "Hello World"`.

Happy orchestrating!
