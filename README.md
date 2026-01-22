# Fahrgemeinschaften

## Overview

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [automatic (Debian based only)](#automatic)
  - [Docker](#docker)
- [To Do](#to-do)
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

## To Do

- [ ] automaticly assign users to drives based on their locactions, prefer the users with least detour
- [ ] scedule drives (Monday, Thursday, Saturday) repete for a period of time
- [ ] Filters for drives
- [ ] App mit React Native
- [ ] Open Street Map integration
- [ ] Untis Integration für automatisch Stunden
- [ ] remove flashbang [tailwind](https://tailwindcss.com/docs/installation/tailwind-cli)
- [ ] fix secruity issues (XSS) and take a look at [Flask Secruity](https://flask.palletsprojects.com/en/stable/web-security/)

## Credits

- Logo made by [MagierderSteine](https://github.com/MagierderSteine)
