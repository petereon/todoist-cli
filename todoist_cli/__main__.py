from typing import List, Optional
import typer
from rich.console import Console
from todoist_api_python.api import TodoistAPI

from utils import format_tasks, get_token

app = typer.Typer(no_args_is_help=True, short_help=True)
console = Console()
api = None

@app.command(name="list")
def list_tasks(filter: Optional[str] = typer.Option(None), order: Optional[List[str]] = typer.Option(None)):
    tasks_response = api.get_tasks(filter=filter)
    labels_response = api.get_labels()
    renderable = format_tasks(tasks=tasks_response, labels=labels_response, orderings=order)
    console.print(renderable)

@app.command()
def create_task():
    pass

if __name__ == "__main__":
    token = get_token()
        
    api = TodoistAPI(token)

    app()