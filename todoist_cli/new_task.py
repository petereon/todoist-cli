priority_to_num = {
    "P1": 4,
    "P2": 3,
    "P3": 2,
    "P4": 1,
}


def preprocess_task_metadata(labels, labels_response, project, projects_response, priority):
    return (find_label_ids(labels, labels_response), 
            find_project_id(project, projects_response), 
            priority_to_num.get(priority.upper(), None))

def find_label_ids(labels, labels_response):
    label_ids = []
    # TODO: handle scenario when label does not exist
    # TODO: include interactive label selector
    for label in labels_response:
        if label.name in labels: 
            label_ids.append(label.id)
    return label_ids
            
def find_project_id(project, projects_response):
    project_id = None
    # TODO: handle scenario when project does not exist
    # TODO: include interactive project selector
    for project_ in projects_response:
        if project == project_.name:
            project_id = project_.id
    return project_id