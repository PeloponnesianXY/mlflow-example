# Containers Learning Plan

This guide is for learning containers using this project.

## Big Idea

Think of a container like a lunchbox for code.

- Your app goes in the lunchbox.
- Its tools go in the lunchbox.
- Anyone with Docker can open the same lunchbox and run the same app.

That means fewer "it works on my machine" problems.

## What You Need To Install

Because you are on Windows, install:

1. Docker Desktop
2. WSL 2 if Docker Desktop asks for it

You do not need to learn Kubernetes or cloud stuff yet.
Just Docker Desktop is enough for this stage.

## What We Are Learning In Order

### Stage 1: Learn the words

Goal: understand the basic pieces.

You should know these words:

- `image`: a saved recipe
- `container`: a running copy of that recipe
- `Dockerfile`: the instructions for building the recipe
- `volume`: a folder that survives when the container stops
- `port`: a door that lets your browser talk to the app

### Stage 2: Containerize one training script

Goal: put `train.py` in a container and run it.

You will learn:

- how to write a small `Dockerfile`
- how to copy code into the image
- how to install Python packages in the image
- how to run `python train.py`

### Stage 3: Keep MLflow results outside the container

Goal: make `mlruns` and `mlflow.db` stay on your computer.

You will learn:

- why containers are disposable
- why experiment data should live in mounted folders
- how to use volume mounts

### Stage 4: Run the MLflow UI in a container

Goal: open MLflow in your browser from a container.

You will learn:

- how to map a container port to your computer
- how to run the UI with access to your experiment files

### Stage 5: Use `docker compose`

Goal: stop typing long Docker commands.

You will learn:

- how to define services in one file
- how to start and stop the stack with one command

## The Learning Path For This Repo

### Lesson 1: Understand what already exists

This repo currently has:

- `train.py`: a scikit-learn wine example
- `fashion_train.py`: a PyTorch Fashion-MNIST example
- `mlruns/`: MLflow run history
- `mlflow.db`: local MLflow database

This is good for container practice because it has both training code and tracking output.

### Lesson 2: Start with the easiest target

Start with `train.py`, not `fashion_train.py`.

Why:

- it is smaller
- it has fewer dependencies
- it does not need dataset downloads during the first container lesson

### Lesson 3: Add a simple Dockerfile

First goal:

- build an image
- run `train.py`
- confirm it creates or updates MLflow artifacts

### Lesson 4: Mount local data

Next goal:

- mount `mlruns`
- mount `mlflow.db`
- rerun training
- confirm results still exist after the container exits

### Lesson 5: Containerize the UI

Next goal:

- run MLflow UI in Docker
- visit it in the browser
- inspect your training runs

### Lesson 6: Compose the workflow

Final beginner goal:

- one service for training jobs
- one service for the MLflow UI
- one compose file to manage both

## What To Install First

Do this before we write Docker files:

1. Install Docker Desktop for Windows
2. Open Docker Desktop once and finish setup
3. Make sure it says Docker is running
4. In PowerShell, run `docker --version`
5. In PowerShell, run `docker compose version`

If either command fails, stop there and fix Docker before doing anything else.

## How We Should Work Together

We should do this one tiny step at a time:

1. Install Docker Desktop
2. Verify Docker works
3. Add a beginner `Dockerfile`
4. Build the image
5. Run `train.py` in the container
6. Add volume mounts
7. Add MLflow UI container
8. Add `docker-compose.yml`

## What I Recommend Next

Your next action is only this:

Install Docker Desktop and then tell me the output of:

- `docker --version`
- `docker compose version`

After that, I will guide you through the first real container file for this repo.
