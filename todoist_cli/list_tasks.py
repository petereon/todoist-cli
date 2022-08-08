from datetime import datetime
from typing import List

import pytz
from rich.console import ConsoleRenderable
from rich.table import Table

priority_colors = {
    4: "[bold red1]P1[/bold red1]",
    3: "[bold orange1]P2[/bold orange1]",
    2: "[blue1]P3[/blue1]",
    1: "P4",
}

color_format = {
    30: "[deep_pink4]{}[/deep_pink4]",
    31: "[red1]{}[/red1]",
    32: "[orange1]{}[/orange1]",
    33: "[gold1]{}[/gold1]",
    34: "[dark_olive_green3]{}[/dark_olive_green3]",
    35: "[chartreuse3]{}[/chartreuse3]",
    36: "[green3]{}[/green3]",
    37: "[dark_turquoise]{}[/dark_turquoise]",
    38: "[deep_sky_blue3]{}[/deep_sky_blue3]",
    39: "[deep_sky_blue1]{}[/deep_sky_blue1]",
    40: "[sky_blue2]{}[/sky_blue2]",
    41: "[royal_blue1]{}[/royal_blue1]",
    42: "[slate_blue1]{}[/slate_blue1]",
    43: "[purple]{}[purple]",
    44: "[plum3]{}[/plum3]",
    45: "[deep_pink3]{}[/deep_pink3]",
    46: "[pale_violet_red1]{}[/pale_violet_red1]",
    47: "[grey35]{}[/grey35]",
    48: "[grey74]{}[/grey74]",
    49: "[tan]{}[/tan]",
}


def render_tasks(
    tasks, labels, projects, orderings: List[str], short
) -> ConsoleRenderable:
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

    for task in tasks:
        row = []
        if not short:
            row.append(str(task.id))
            row.append(render_project(task.project_id, projects))
        row.append(render_datetime(task))
        row.append("[bold bright_white]" + task.content + "[/bold bright_white]")
        row.append(priority_colors[task.priority])
        row.append(", ".join(render_labels(label_ids=task.label_ids, labels=labels)))
        table.add_row(*row)

    return table


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


def render_labels(label_ids: List[int], labels):
    labels_repr = []
    for label in labels:
        if label.id in label_ids:
            labels_repr.append(color_format[label.color].format("@" + label.name))

    return labels_repr


def render_project(project_id, projects):
    for project in projects:
        if project.id == project_id:
            return color_format[project.color].format("#" + project.name)
