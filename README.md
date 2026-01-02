# Fahrgemeinschaften

## Overview

## Tech Stack

Frontend:
- HTML, Tailwind, Javascript\
Backend:
- Programmiersprache: Python
- Framework: Flask
- Datenbank: Postgres\
Extra‘s:
- Docker Image
- App mit React Native
- Open Street Map integration
- Untis Integration für automatisch Stunden

## Features
- setup.sh for quick setup on server
- Login
- register
- list of all availible routes
- docker compose with database
- setup.sh to install docker on ubuntu based distro's and build the image and start the docker compose.yml

## Issues
~~- duplicates of routes when logout and login again~~

## To Do
- [ ] Filters for the drives
- [ ] Edit route page


## getting started
- create a .env file in the root directory of the projekt and insert the following into it

```sh
PG_USERNAME=
PG_PASSWORD=
PG_DATABASE=
PG_HOST=

PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=

FLASK_SECRET_KEY=
```

then you have to make sure to fill it with values. 
The you need to give permissions to execute the setup.sh file.
```sh
chmod +x setup.sh
```

and the execute it:
```sh
./setup.sh
```
Now the postgres database will be running on port `5432`, pgadmin on port `80` and the main app called Fahrgemeinschaften on Port `5000`.


## Manual Install
To create the Docker Imgae by yourself you need to run:
```sh
docker build -t fahrgemeinschaften .
```

and then run
```sh
docker compose up -d
```

## Ressources
Login:
<https://flowbite.com/blocks/marketing/login/>



## Credits:
- Logo made by [MagierderSteine](https://github.com/MagierderSteine?tab=overview&from=2025-12-01&to=2025-12-25)
# Fahrgemeinschaften
# Fahrgemeinschaften
