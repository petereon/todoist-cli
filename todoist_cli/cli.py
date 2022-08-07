#!/usr/bin/env python

from typing import List, Optional
import typer
from rich.console import Console
from todoist_api_python.api import TodoistAPI

from todoist_cli.utils import render_tasks, get_token, preprocess_task_metadata

app = typer.Typer(no_args_is_help=True, short_help=True)
console = Console()
api = None

def cli():
    global api
    token = get_token() 
    api = TodoistAPI(token)
    app()

@app.command(name="list")
def list_tasks(filter: Optional[str] = typer.Option(None), order: Optional[List[str]] = typer.Option(None)):
    global api
    tasks_response = api.get_tasks(filter=filter)
    labels_response = api.get_labels()
    renderable = render_tasks(tasks=tasks_response, labels=labels_response, orderings=order)
    console.print(renderable)

@app.command(name="new-task")
def new_task(content: str = typer.Argument('new task'),
             description: Optional[str] = typer.Option(None),
             priority: Optional[str] = typer.Option(None),
             label: Optional[List[str]] = typer.Option(None), 
             project: Optional[str] = typer.Option(None),
             date: Optional[str] = typer.Option(None)):
    global api
    labels_response = api.get_labels()
    projects_response = api.get_projects()
    task_metadata = preprocess_task_metadata(labels=label, 
                                             labels_response=labels_response, 
                                             project=project, 
                                             projects_response=projects_response, 
                                             priority=priority)
    
    api.add_task(content=content, 
                 description=description, 
                 label_ids=task_metadata[0], 
                 project_id=task_metadata[1], 
                 priority=task_metadata[2],
                 due_string=date)

