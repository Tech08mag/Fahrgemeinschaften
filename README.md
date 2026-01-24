# Fahrgemeinschaften

## Overview

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [automatic (Debian based only)](#automatic)
  - [Docker](#docker)
  - [dev](#dev)
    - [styling](#styling)
    - [Database](#database)
    - [backend](#backend)
- [To Do](#to-do)
- [Preview](#preview)
- [Credits](#credits)

## Tech Stack

- Python with Flask for the backend
- HTML files with Tailwind Components
- Postgres Database

## Installation

For the Docker install, docker compose needs to be installed and uv for the python backend\
Create in the root of the project a .env file with the following content:

```env
PG_USERNAME=
PG_PASSWORD=
PG_DATABASE=
PG_HOST=

FLASK_SECRET_KEY=
```

For an automatic install of the dependencies and an automatic build and start of the projct you could run: (this works only on debian based distro's):\
First make the file executable

### automatic

```sh
chmod +x setup.sh
```

run the file

```sh
./setup.sh
```

Now the main application run on port `5000` and the Database on Port `5432`

### Docker

```sh
docker build -t fahrgemeinschaften .
```

and then run

```sh
docker compose up -d
```

### dev

#### Styling

Install tailwind standalone:

```sh
npm install tailwindcss @tailwindcss/cli
```

compile the css and the changes:

```sh
npx @tailwindcss/cli -i ./static/styles/main.css -o ./static/styles/output.css --watch
```

#### Database

create a Folder called `db_test` and create a `docker-compose.yml`and insert the following content:

```docker
services:
  postgres:
    container_name: container-pg
    image: postgres:latest
    hostname: postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: ${PG_USERNAME}
      POSTGRES_PASSWORD: ${PG_PASSWORD}
      POSTGRES_DB: ${PG_DATABASE}
    volumes:
      - ./data:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${PG_USERNAME}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    restart: unless-stopped
```

then add a `.env` file with the following content:

```sh
# those are example values please don't use them in production
PG_USERNAME=postgres
PG_PASSWORD=postgres
PG_DATABASE=postgres
PG_HOST=localhost
```

then run:

```sh
docker compose up
```

#### backend

Install uv

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

then start the flask server (this action will fail if the database is not poperly configured or running):

```sh
uv run main.py
```

## To Do

- [ ] automaticly assign users to drives based on their locactions, prefer the users with least detour
- [ ] scedule drives (Monday, Thursday, Saturday) repeate for a period of time
- [ ] App mit [cordova](https://cordova.apache.org/#getstarted)
- [ ] Open Street Map integration
- [ ] Untis Integration für automatisch Stunden

## Preview

!["index.png"](/project-preview/index.png)
!["login.png"](/project-preview/login.png)
!["register.png"](/project-preview/register.png)
!["drive overview.png"](/project-preview/drive_overview.png)
!["edit drive.png"](/project-preview/edit_drive.png)
!["my_drives.png"](/project-preview/my_drives.png)
!["my_drives_with_test_drive.png"](/project-preview/my_drives_with_test_drive.png)
!["passenger.png"](/project-preview/passengers.png)
!["settings.png"](/project-preview/settings.png)

## Credits

- Logo made by [MagierderSteine](https://github.com/MagierderSteine)
