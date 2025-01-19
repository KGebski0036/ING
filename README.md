# ING

OPIS

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

- [Logs Humanizer](scripts/logs_humanizer.py) - script to humanize logs and goupoing them by ip address
- [Logs Generator](scripts/logs_generator.py) - script to generate  random logs
- [Create Model](scripts/create_model.py) - script to create a AI model for analyzing logs 
- [Analyze Logs](scripts/analyze_logs.py) - script to analyze logs using created AI model

## How to start program

### Linux

#### Requirements
```
sudo apt install make python3 python3.11-venv
```

After downoadin this repository start a terminal inside it.
```bash
$ python3 -m venv ing
$ source ing/bin/activate
$ pip install -r requirements.txt
$ make create_model
```