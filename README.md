# Private
Private privacy preserving analysis language

## Installation
Use python setuptools:
```bash
python setup.py install
```

## Usage
To open an interactive session
```bash
cd Private
python command.py
```

To run commands from a file
```bash
python command.py yourCommandsFile.pr
```

## Run on Docker
1) Install docker-compose: https://docs.docker.com/compose/


2) Initial build and deploy services:
```bash
docker-compose up --build

#Note: Subsequent deployments can be run with:
docker-compose up
```

3) Shutdown services:
```bash
docker-compose down
```

## Tutorials
More examples of how to use Private are contained in the tutorials directory

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)



