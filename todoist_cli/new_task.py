import cutie

priority_to_num = {
    "P1": 4,
    "P2": 3,
    "P3": 2,
    "P4": 1,
}


def preprocess_task_metadata(
    labels, labels_response, project, projects_response, priority, interactive
):
    return (
        find_label_ids(labels, labels_response, interactive),
        find_project_id(project, projects_response, interactive),
        find_priority(priority, priority_to_num, interactive),
    )


def find_label_ids(labels, labels_response, interactive):
    label_ids = []
    if interactive and not labels:
        print("\nSelect label(s):\n")
        all_labels = ["@" + label.name for label in labels_response]
        labels = [
            all_labels[i].replace("@", "")
            for i in cutie.select_multiple(all_labels, hide_confirm=True)
        ]
    for label in labels_response:
        if label.name in labels:
            labels.remove(label.name)
            label_ids.append(label.id)
    if labels:
        print("\nLabel(s) not found: {}".format(", ".join(labels)))
        if not cutie.prompt_yes_or_no(
            "Do you want to continue without labels {}".format(", ".join(labels))
        ):
            raise Exception("Label(s) not found: {}".format(", ".join(labels)))
    return label_ids


def find_project_id(project, projects_response, interactive):
    project_id = None
    if interactive and not project:
        print("\nSelect a project:")
        all_projects = ["#" + project.name for project in projects_response]
        project = all_projects[cutie.select(all_projects)].replace("#", "")
    for project_ in projects_response:
        if project == project_.name:
            project_id = project_.id
    if project and not project_id:
        print("\nProject not found: {}".format(project))
        if not cutie.prompt_yes_or_no("Do you want to continue with no project"):
            raise Exception("Project not found: {}".format(project))
    return project_id


def find_priority(priority, priority_to_num, interactive):
    priorities = [None] + list(priority_to_num.keys())
    if not priority and interactive:
        print("\nSelect a priority:")
        priority = priorities[cutie.select(priorities)]
    if priority and priority.upper() not in priorities:
        print("\nInvalid priority: {}".format(priority))
        if not cutie.prompt_yes_or_no("Do you want to continue with no priority"):
            raise Exception("Invalid priority: {}".format(priority))
    return priority_to_num.get(priority)
