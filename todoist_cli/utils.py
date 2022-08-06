from typing import List
from rich.table import Table
from rich.panel import Panel
from rich.console import ConsoleRenderable
from datetime import datetime, timezone
import pytz

priority_colors = {
    4: "[bold red1]P1[/bold red1]",
    3: "[bold orange1]P2[/bold orange1]",
    2: "[blue1]P3[/blue1]",
    1: "P4"
}

label_format = {
    30 : "[deep_pink4]{}[/deep_pink4]",
    31 : "[red1]{}[/red1]",
    32 : "[orange1]{}[/orange1]",
    33 : "[gold1]{}[/gold1]",
    34 : "[dark_olive_green3]{}[/dark_olive_green3]",
    35 : "[chartreuse3]{}[/chartreuse3]",
    36 : "[green3]{}[/green3]",
    37 : "[dark_turquoise]{}[/dark_turquoise]",
    38 : "[deep_sky_blue3]{}[/deep_sky_blue3]",
    39 : "[deep_sky_blue1]{}[/deep_sky_blue1]",
    40 : "[sky_blue2]{}[/sky_blue2]",
    41 : "[royal_blue1]{}[/royal_blue1]",
    42 : "[slate_blue1]{}[/slate_blue1]",
    43 : "[purple]{}[purple]",
    44 : "[plum3]{}[/plum3]",
    45 : "[deep_pink3]{}[/deep_pink3]",
    46 : "[pale_violet_red1]{}[/pale_violet_red1]",
    47 : "[grey35]{}[/grey35]",
    48 : "[grey74]{}[/grey74]",
    49 : "[tan]{}[/tan]"
}

def read_and_close(f):
    s = f.read()
    f.close()
    return s

def get_token():
    import os
    home = os.getenv('HOME')
    path = f'{home}/.todoist_token'
    if not os.getenv("TODOIST_API_TOKEN") and not os.path.exists(path):
        token = typer.prompt('Todoist API token', hide_input=True)
        if typer.prompt('Save to file? (Y/n)').upper() == 'Y':
            
            print(f'Saving the token to {path}')
            f = open(path, "w")
            f.write(token)
            f.close()
        else:
            print('Saving the token to environment variable `TODOIST_API_TOKEN`')
            os.environ["TODOIST_API_TOKEN"] = token
    else:
        token = os.getenv("TODOIST_API_TOKEN") or read_and_close(open(path, 'r'))
    
    return token

def format_tasks(tasks, labels, orderings: List[str]=None) -> ConsoleRenderable:
    table = Table(title=None, box=None, header_style="bold green", title_justify='left', show_header=False)
    table.add_column("")
    table.add_column("", style='bold bright_white')
    table.add_column("")
    table.add_column("")
    
    if orderings:
        for ordering in reversed(orderings):
            if ordering in ['p', 'P', 'Priority', 'priority']:
                tasks = sorted(tasks, key=lambda task: task.priority, reverse=True)
            if ordering in ['date', 'Date' , 'time', 'Time', 'd', 'D', 't', 'T']:
                tasks = sorted(tasks, key=lambda task: task.due.datetime)
    
    
    for task in tasks:
        table.add_row(preprocess_datetime(task), task.content, priority_colors[task.priority], process_labels(label_ids=task.label_ids, labels=labels))
    
    return table

def preprocess_datetime(task):
    tz = pytz.timezone(task.due.timezone)
    task_datetime = tz.fromutc(datetime.strptime(task.due.datetime, '%Y-%m-%dT%H:%M:%SZ'))
    formatted_datetime = datetime.strftime(task_datetime, "%a %H:%M:%S")
    if task_datetime < datetime.now(tz=tz):
        formatted_datetime = f'[red1]{formatted_datetime}[/red1]'
        
    return formatted_datetime

def process_labels(label_ids: List[int], labels):
    labels_repr = []
    for label in labels: 
        if label.id in label_ids:
            labels_repr.append(label_format[label.color].format('@'+label.name))
            
    return ', '.join(labels_repr)
    