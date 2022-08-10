from todoist_cli.list_tasks import render_tasks
import cutie


def select_task(tasks, labels, projects, console):
    renderable = render_tasks(
        tasks=tasks,
        labels=labels,
        projects=projects,
        orderings=["t"],
        short=False,
    )
    with console.capture() as captured:
        console.print(renderable)
    options = captured.get().split("\n")[:-1]

    return int(renderable.columns[0]._cells[cutie.select(options)])
