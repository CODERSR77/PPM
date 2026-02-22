# Copyright (C) 2026 <Your Name/Username>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path
import os
from click import confirm
import typer
from typing import Optional
import shutil
import subprocess

app = typer.Typer()

#File System
workspace = Path("~/.ppm").expanduser()

@app.command()
def create(project_name: str):
    new_project = workspace / project_name
    new_project.mkdir(parents=True)
    init_uv = subprocess.run(["uv","init"],cwd=new_project,capture_output=True,text=True)
    typer.echo(f"{project_name} successfully created!")
    typer.echo(init_uv)

@app.command()
def remove(project_name: str):
    dir_getting_removed = workspace / project_name
    conformatiom = input(f"Are you sure you wan to remove {dir_getting_removed.name} (y/n): ")
    if conformatiom.lower() == "y":
        shutil.rmtree(dir_getting_removed)
        typer.echo(f"{dir_getting_removed} was successfully removed!")
    else:
        typer.echo(f"{dir_getting_removed} was not removed")
@app.command()
def sync(project_name: Optional[str] = typer.Argument(None)):
    if project_name:
        project_dir = workspace / project_name
        env = os.environ.copy()
        env.pop("VIRTUAL_ENV", None)
        result = subprocess.run(["uv","sync"],cwd=project_dir,capture_output=True,text=True,env=env)
        typer.echo(result)
    else:
        project_dirs = []
        for i in workspace.iterdir():
            project_dirs.append(i)
        for i in project_dirs:
            env = os.environ.copy()
            env.pop("VIRTUAL_ENV",None)
            result = subprocess.run(["uv","sync"],cwd=i,capture_output=True,text=True,env=env)
            typer.echo(f"{i} was successfully synced")
            typer.echo(f"Given output: {result.stdout}")
            typer.echo(f"Given error: {result.stderr}")
@app.command()
def list():
    for i in workspace.iterdir():
         typer.echo(i.name)

if __name__ == "__main__":
    app()
