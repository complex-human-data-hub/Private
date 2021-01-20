# Private
Private privacy preserving analysis language

## Run on Docker
1) Install the docker engine and docker-compose. 

- Docker engine: https://docs.docker.com/engine/install/

- Docker-Compose: https://docs.docker.com/compose/install (separate install is only necessarily on Linux, on other OSs docker-compose is bundled with Docker Desktop)


2) Initial build and deploy services:
```bash
docker-compose up --build

#Note: Subsequent deployments can be run with:
docker-compose up
```

You will now be able to access Private on:
http://localhost:5000/


3) Shutdown services:
```bash
docker-compose down
```

## Tutorials
More examples of how to use Private can be found on Simon Dennis' blog:
https://simondennis.blog/category/private/


## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)



