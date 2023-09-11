# A simple yet detailed FastAPI App project

<img src="app/static/images/Logo_Data_Engineering_101.png" width=50% height=50%>\
This repository contains a FastAPI web application for training purpose 📚.\
The app is composed of a FastAPI-SQLAlchemy-PostgreSQL backend combined with a server side render Jinja2.\
Here is the project's schema architecture :\
![Alt text](/project_architecture.png?raw=true "Project architecture")
<!-- ![Schema Architecture](project_architecture.png) -->

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Deployment](#deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Reference](#api-reference)
- [Lessons learned](#lessons-learned)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Python](https://www.python.org/downloads/) (3.9 or higher)
- [Docker](https://www.docker.com/products/docker-desktop)
- [GitHub account](https://github.com/)

## Setup
Clone the repository then go to the root directory :

   ```bash
   git clone https://github.com/Stephd91/FastAPI.git
   cd FastAPI
   ```

Build the Docker Image. The docker build command uses the Dockerfile to build a new image.
Then run the application in a Container using the docker run command.

  ```bash
  docker build -t fastapiproject .
  docker run -d --name fastapicontainer -p 80:80 fastapiproject
  ```
Verify the deployment by navigating to your server address in your preferred browser.
Frontend, built with Docker, with routes handled based on the path: http://localhost:80
Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:80/docs
  ```bash
  127.0.0.1:80
  ```
## CI/CD Pipeline
Automatically build and tag a Docker image and test it with GitHub Actions
1. Go to your GitHub repo > Actions tab
2. Select set up a workflow yourself. This takes you to a page for creating a new GitHub actions workflow file in your repository, under .github/workflows/main.yml by default.
3. In the editor window, copy and paste the following YAML configuration :
  ```bash
  To do
  ```

## API Reference

#### Get the homepage

```http
  GET /app
```
Render the homepage app.html from Jinja2 to navigate through cards and their associated themes, go the other routes from here (create a card, launch a flash-session)

#### Get flash session through UI

```http
  POST /flash-session
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `theme(s)`      | `string` | **Required**. List of themes selected in the "Start Flash Session"popup  |
| `num_cards`      | `int` | **Required**. Nb of cards selected in the "Start Flash Session"popup |

#### Create a card through UI
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
* 📌 **Database skills**:
  * ✅ PostgreSQL handling with CLI
  * ✅ UML diagram and entity relationships in a relational database
  * ✅ Alembic migrations
* 📌 **Python & API skills** :
  * ✅ SQLALchemy ORM language
  * ✅ Endpoint logic with FastAPI and crud operations
  * ✅ Pydantic model validation
  * ✅ Unit testing with pytest
* 📌 **Front-end skills** :
  * ✅ Some Bootstrap, HTML and Javascript coding
* 📌 **Deployment skills** :
  * ✅ Used "decouple" package to hide connection infos with environment variables
  * ✅ Dockerization
  * ✅ CI/CD pipeline with GitHub Actions

