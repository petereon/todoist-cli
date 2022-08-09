#!/usr/bin/env python

from typing import List, Optional
import typer
from rich.console import Console
from todoist_api_python.api import TodoistAPI

from todoist_cli.utils import get_token, maybe_end_spinner, mayber_start_spinner
from todoist_cli.list_tasks import render_tasks
from todoist_cli.new_task import preprocess_task_metadata

app = typer.Typer(no_args_is_help=True, short_help=True)
console = Console()
api = None


def cli():
    global api
    token = get_token()
    api = TodoistAPI(token)
    app()


@app.command(name="list")
def list_tasks(
    filter: Optional[str] = typer.Option(
        None, "--filter", "-f", help="Filter for tasks e.g. '(overdue|today)'"
    ),
    order: Optional[List[str]] = typer.Option(
        None,
        "--order",
        "-o",
        help="Ordering(s) for the tasks, accepted values are `time` or `t` and `priority` or `p`",
    ),
    short: Optional[bool] = typer.Option(
        False,
        "--short",
        "-s",
        is_flag=True,
        help="Will display only short version of table (date, task content, priority and labels)",
    ),
    interactive: Optional[bool] = typer.Option(
        True,
        "-i/-n",
        "--interactive/--no-interactive",
        is_flag=True,
        help="Interactive mode",
    ),
):
    global api
    status_context = console.status('Fetching info from API...')
    if interactive:
        status_context.__enter__()
    tasks_response = api.get_tasks(filter=filter)
    labels_response = api.get_labels()
    projects_response = api.get_projects()
    if interactive:
        status_context.__exit__(None,None,None)
    renderable = render_tasks(
        tasks=tasks_response,
        labels=labels_response,
        projects=projects_response,
        orderings=order,
        short=short,
    )
    console.print(renderable)


@app.command(name="new")
def new_task(
    content: str = typer.Argument("New task", help="Content of the task"),
    description: Optional[str] = typer.Option(
        None, "--desc", "--description", "-s", help="Long description for the task"
    ),
    priority: Optional[str] = typer.Option(
        None,
        "--prio",
        "--priority",
        "-p",
        help="Priority for the task, accepted values are `P1`, `P2`, `P3` and `P4`",
    ),
    label: Optional[List[str]] = typer.Option(
        None, "--label", "-l", help="Label(s) for the task"
    ),
    project: Optional[str] = typer.Option(
        None,
        "--project",
        "-r",
        help="Project that task should belong under, default is Inbox",
    ),
    date: Optional[str] = typer.Option(
        None,
        "--date",
        "-d",
        help="Date time for tasks (accepts all the date formats allowed in Todoist interface in plain text)",
    ),
    interactive: Optional[bool] = typer.Option(
        True,
        "-i/-n",
        "--interactive/--no-interactive",
        is_flag=True,
        help="Interactive mode",
    ),
):
    global api
    status_context = mayber_start_spinner('Fetching info from API...', interactive, console)
    labels_response = api.get_labels()
    projects_response = api.get_projects()
    maybe_end_spinner(status_context, interactive)

    if interactive and not content:
        content = typer.prompt("Provide content for the task")

    if interactive and not description:
        description = typer.prompt("Provide description for the task")

    if interactive and not date:
        date = typer.prompt("Provide date (any datestring that Todoist handles works)")

    task_metadata = preprocess_task_metadata(
        labels=label,
        labels_response=labels_response,
        project=project,
        projects_response=projects_response,
        priority=priority,
        interactive=interactive,
    )

    status_context = mayber_start_spinner('Creating a task...', interactive, console)
    api.add_task(
        content=content,
        description=description,
        label_ids=task_metadata[0],
        project_id=task_metadata[1],
        priority=task_metadata[2],
        due_string=date,
    )
    maybe_end_spinner(status_context, interactive)
