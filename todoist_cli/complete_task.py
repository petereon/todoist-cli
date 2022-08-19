from todoist_cli.list_tasks import render_tasks
import beaupy


def select_task(tasks, labels, projects, console):
    rendered_tasks = render_tasks(
        tasks=tasks,
        labels=labels,
        projects=projects,
        orderings=["t"],
        short=False,
    )
    
    max_len_content = max([len(task[3]) for task in rendered_tasks])
    task_strings = []
    for task in rendered_tasks:
        task[3] = task[3] + (max_len_content - len(task[3])) * ' '
        task[2] = task[2] + (25 - len(task[2])) * ' '
        task_repr = ' '.join(task)
        task_strings.append(task_repr)

    return int([task[0] for task in rendered_tasks][beaupy.select(task_strings, return_index=True)])
