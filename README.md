# A simple yet detailed FastAPI App project
![Logo](app/static/images/Logo_Data_Engineering_101.png)
This repository contains a FastAPI web application for training purpose 📚. \
The app is composed of a FastAPI-SQLAlchemy-PostgreSQL backend combined with a server side render Jinja2. \
Here is the project's schema architecture :
![Alt text](/project_architecture.png?raw=true "Project architecture")
![Schema Architecture](project_architecture.png)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker](#docker)
- [API Reference](#api-reference)
- [Lessons learned](#lessons-learned)
- [Deployment](#deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Python](https://www.python.org/downloads/) (3.7 or higher)
- [Docker](https://www.docker.com/products/docker-desktop)
- [GitHub account](https://github.com/)

## Local Development
Clone the repository then go to the project directory :

   ```bash
   git clone https://github.com/Stephd91/FastAPI.git
   cd FastAPI
   ```

## Docker
Build then run the Docker Image to a container:

  ```bash
  docker build -t FastAPI .
  docker run -d --name mycontainer -p 80:80 FastAPI
  ```

## API Reference

#### Get the homepage

```http
  GET /app
```
Render the homepage app.html from Jinja2 to navigate through cards and their associated themes, go the other routes from here (create a card, launch a flash-session)

#### Get flash session

```http
  POST /flash-session
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `theme(s)`      | `string` | **Required**. List of themes selected in the "Start Flash Session"popup  |
| `num_cards`      | `int` | **Required**. Nb of cards selected in the "Start Flash Session"popup |

#### Create a card
```http
  POST /create-card
```

#### Modify a card
```http
  PUT /modify-card/{card_id}
```

#### Delete a card
```http
  DELETE /delete-card/{card_id}
```


## Lessons Learned

Building this project from scratch, I could learn a lot about how API is built to exchange with its clients and its backend database.
Here are the skills I learned from this project :
📌 Database skills : 
    ✅ PostgreSQL handling with CLI
    ✅ UML diagram and entity relationships in a relational database
    ✅ Alembic migrations
📌 Python & API skills : 
    ✅ SQLALchemy ORM language
    ✅ Endpoint logic with FastAPI and crud operations
    ✅ Pydantic model validation 
    ✅ Unit testing with pytest
📌 Front-end skills :
    ✅ Some Bootstrap, HTML and Javascript coding
📌 Deployment skills :
    ✅ Used decouple with environment variables to hide connection infos
    ✅ Dockerization
    ✅ CI/CD pipeline with GitHub Actions

