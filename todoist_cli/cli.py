#!/usr/bin/env python

from typing import List, Optional
import typer
from rich.console import Console
from todoist_api_python.api import TodoistAPI
from todoist_cli.complete_task import select_task

from todoist_cli.utils import get_token
from todoist_cli.list_tasks import tabularize_tasks
from todoist_cli.new_task import preprocess_task_metadata

app = typer.Typer(
    no_args_is_help=True,
    short_help=True,
    help="A CLI tool listing and creating a Todoist tasks.",
)
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
):
    global api
    with console.status("Fetching info from API..."):
        tasks_response = api.get_tasks(filter=filter)
        labels_response = api.get_labels()
        projects_response = api.get_projects()
    renderable = tabularize_tasks(
        tasks=tasks_response,
        labels=labels_response,
        projects=projects_response,
        orderings=order,
        short=short,
    )
    console.print(renderable)

    with console.capture() as captured:
        console.print(renderable)


@app.command(name="new")
def new_task(
    content: str = typer.Argument(None, help="Content of the task"),
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
    with console.status("Fetching info from API..."):
        labels_response = api.get_labels()
        projects_response = api.get_projects()

    if interactive and not content:
        content = typer.prompt("Provide content for the task")

    if interactive and not description:
        description = typer.prompt("Provide description for the task", default="")

    if interactive and not date:
        date = typer.prompt(
            "Provide date (any datestring that Todoist handles works)", default=""
        )

    task_metadata = preprocess_task_metadata(
        labels=label,
        labels_response=labels_response,
        project=project,
        projects_response=projects_response,
        priority=priority,
        interactive=interactive,
    )
    with console.status("Creating task..."):
        api.add_task(
            content=content,
            description=description,
            label_ids=task_metadata[0],
            project_id=task_metadata[1],
            priority=task_metadata[2],
            due_string=date,
        )


@app.command(name="complete")
def complete_task(
    task_id: Optional[int] = typer.Argument(None, help="ID of the task to complete"),
    interactive: Optional[bool] = typer.Option(
        True,
        "-i/-n",
        "--interactive/--no-interactive",
        is_flag=True,
        help="Interactive mode",
    ),
):
    global api
    if not task_id:
        if interactive:
            with console.status("Fetching info from API..."):
                tasks_response = api.get_tasks(filter="(today|overdue)")
                labels_response = api.get_labels()
                projects_response = api.get_projects()
            task_id = select_task(
                tasks=tasks_response,
                labels=labels_response,
                projects=projects_response,
                console=console,
            )

        else:
            raise Exception("No task ID provided")
    with console.status("Completing task..."):
        api.close_task(task_id=task_id)
