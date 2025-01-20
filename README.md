# WH - RoarING Success

This repository contains a solution for the anomaly detection task in IT systems. The project includes:

- Log Analysis: Processing and analyzing a log file containing records of system activities, including both normal operations and potential anomalies.
- AI Model Development: Building an AI-powered detection system capable of identifying attacks.

This solution is designed for use in IT security monitoring systems.

## Collaborators
<div align="center">
    <a href="https://github.com/BartoszBareja"><img src="https://avatars.githubusercontent.com/u/92011808?v=4" height="30" alt="BartoszBareja"  /></a>
    <a href="https://github.com/KGebski0036"><img src="https://avatars.githubusercontent.com/u/57415454?v=4" height="30" alt="KGebski0036"  /></a>
    <a href="https://github.com/bberni"><img src="https://avatars.githubusercontent.com/u/63294458?v=4" height="30" alt="bberni"  /></a>
    <a href="https://github.com/MikPisula"><img src="https://avatars.githubusercontent.com/u/47534140?v=4" height="30" alt="MikPisula"  /></a>
</div>

## Tehnologies

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="30" alt="cplusplus  logo"  />

## Contents

- [Logs Humanizer](scripts/logs_humanizer.py) - Script to humanize logs and group them by IP address.
- [Logs Generator](scripts/logs_generator.py) - Script to generate random logs.
- [Create Model](scripts/create_model.py) - Script to create an AI model for analyzing logs.
- [Analyze Logs](scripts/analyze_logs.py) -  Script to analyze logs using the created AI model.

## How to start program

### Linux

#### Requirements
```bash
sudo apt install make python3 python3.11-venv
```

After downloading this repository, start a terminal inside the project directory.

Prepare the environment:
```bash
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Make targets:

>Parameters can be changed inside the Makefile.
```bash
$ make create_model      # Creating new model 
$ make test_model_custom # Generate custom logs and test the model on them
$ make test_model        # Use pre-prepared logs to test the model
$ make humanize_logs     # Convert logs to a human-readable format
$ make clean             # Clear generated logs and models 
```

Script usage:
```bash
$ python3 scripts/analyze_logs.py -f=[FileWitchLogs]
$ python3 scripts/create_model.py -f=[FileWitchLogs]
$ python3 scripts/logs_generator.py -f=[FileWitchLogs] -g=[NumberOfGroups]
$ python3 scripts/logs_humanizer.py -f=[FileWitchLogs]
```