from datetime import datetime
from typing import List

import pytz
from rich.console import ConsoleRenderable
from rich.table import Table

priority_colors = {
    4: "[bold red1]{}[/bold red1]",
    3: "[bold orange1]{}[/bold orange1]",
    2: "[blue1]{}[/blue1]",
    1: "{}",
}

def tabularize_tasks(tasks, labels, projects, orderings: List[str], short):
    table = Table(
        title=None,
        box=None,
        header_style="bold green",
        title_justify="left",
        show_header=False,
    )
    table.add_column("")
    table.add_column("")
    table.add_column("")
    table.add_column("")
    if not short:
        table.add_column("")
        table.add_column("")
    for rendered_task in render_tasks(tasks, labels, projects, orderings, short):
        table.add_row(*rendered_task)
    return table

def render_tasks(
    tasks, labels, projects, orderings: List[str], short
) -> ConsoleRenderable:
    if orderings:
        for ordering in reversed(orderings):
            if ordering in ["p", "P", "Priority", "priority"]:
                tasks = sorted(tasks, key=lambda task: task.priority, reverse=True)
            if ordering in ["date", "Date", "time", "Time", "d", "D", "t", "T"]:
                tasks = sorted(
                    tasks,
                    key=lambda task: task.due.datetime
                    if task.due and task.due.datetime
                    else "9999-99-99",
                )
    rendered_tasks = []
    for task in tasks:
        rendered_task = []
        if not short:
            rendered_task.append(str(task.id))
            rendered_task.append(render_project(task.project_id, projects))
        rendered_task.append(render_datetime(task))
        rendered_task.append(priority_colors[task.priority].format(task.content))
        rendered_task.append(", ".join(render_labels(labels=task.labels)))
        rendered_tasks.append(rendered_task)
    return rendered_tasks


def render_datetime(task):
    if task.due and task.due.datetime:
        tz = pytz.timezone(task.due.timezone)
        task_datetime = tz.fromutc(
            datetime.strptime(task.due.datetime, "%Y-%m-%dT%H:%M:%SZ")
        )
        formatted_datetime = datetime.strftime(task_datetime, "%Y-%m-%d (%a) %H:%M:%S")
        if task_datetime < datetime.now(tz=tz):
            formatted_datetime = f"[red1]{formatted_datetime}[/red1]"

        return formatted_datetime
    return ""


def render_labels(labels: List[str]):
    return [f'@{label}' for label in labels]


def render_project(project_id, projects):
    for project in projects:
        if project.id == project_id:
            return f'[{project.color}]{project.name}[/{project.color}]'
