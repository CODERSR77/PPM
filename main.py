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

from os.path import exists
from pathlib import Path
import os
from click import confirm
import typer
from typing import Optional
import shutil
import subprocess
from enum import Enum
from compression import zstd

app = typer.Typer()

#File System
workspace = Path("~/.ppm").expanduser()
workspace.mkdir(parents=True,exist_ok=True)
backup_dir = Path("~/.ppm-backup").expanduser()
backup_dir.mkdir(parents=True,exist_ok=True)

class CompressionFormat(str,Enum):
    gzip = "gztar"
    zstandard = "zstd"
    xz = "xztar"
    bzip2 = "bztar"
    zip = "zip"

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
def list(a: bool = typer.Option(False,"--all","-a")):
    for i in workspace.iterdir():
         typer.echo(i.name)
    if a:
        for i in backup_dir.iterdir():
            typer.echo(i.name)
@app.command()
def archive(project_name,fmt: CompressionFormat = typer.Option(CompressionFormat.zstandard, "--format", "-f")):
    full_project_name = workspace / project_name 
    archive_base_path = backup_dir / project_name
    venv_dir = full_project_name / ".venv"
    if venv_dir.exists():
        shutil.rmtree(venv_dir)
        typer.echo("The projects .venv was removed")
    if not full_project_name.exists():
        typer.echo("The project doesn't exist")
    else:
        if fmt == CompressionFormat.zstandard:
            tar_path = shutil.make_archive(str(archive_base_path),"tar",root_dir=full_project_name)
            typer.echo("Tarball created...")
            zstd_path  = f"{tar_path}.zst"
            with open(tar_path,"rb") as f_in:
                with zstd.open(zstd_path,"wb") as f_out:
                    shutil.copyfileobj(f_in,f_out)
            typer.echo("Tarball compressed...")
            os.remove(tar_path)
            typer.echo("Temp Tarball removed...")
            shutil.rmtree(full_project_name)
            typer.echo("Removed the project")
        else:
            final_path = shutil.make_archive(str(archive_base_path),fmt.value,root_dir=full_project_name)
            typer.echo("Project compressed...")
            shutil.rmtree(full_project_name)
            typer.echo("Removed project...")

if __name__ == "__main__":
    app()
