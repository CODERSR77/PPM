# PPM(The Python Project Manager)

## Introduction

 PPM is a Python Project Manager it is used to create, delete and manage projects 

## Commands

 Currently it only has 3  commads
```
ppm create <project_name>
```
 create command will create an dir with the name given in ~/.ppm and run uv init in that dir

```
ppm remove <project_name>
```
 remove command will delete the project specified in the ~/.ppm dir
```
ppm sync
```
 or
```
ppm sync <project_name>
```
 The sync command will do 2 things is project name is not specified it will sync every project in the ~/.ppm dir is project name is specified then it will only sync that dir

## Roadmap

I envision adding more commands like find, list, du(disk usage), info, archive etc. I also want to add an feture encrypt the project.

## Contributing

If you liked this project and wanted to help please contribute. Here's how you can help:
* Update the README to be more accurate
* Help in adding fetures like archive, find etc.
* Improve the code with better logic and comments
* Report any issues you had.
* Share this project with more people.

## Tech Stack

* uv
* Typer
* Pathlib
* Subprocess
* Shutil

## Core skills

I think if you know intermediate level of python and have a bit of or more experience with the tools and utils in the Tech Stack section I think your contribution will be very helpful. And Thank you for reading this far.

## Getting Started

### Prerequisites

* Python >=3.14
* UV
### Installation

1. Clone the repo
2. Run `uv sync` inside it
3. Run `uv pip install -e .` inside it
4. Then If on MacOS/Linux run `source .venv/bin/activate` Else If on Windows run `.venv\Scripts\activate`

### Usage

After these steps you can finally just run `ppm sync` and other commands like that
