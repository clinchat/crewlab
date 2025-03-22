import yaml
from task_manager import create_task

def import_tasks_from_yaml(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    created_tasks = []
    for task_data in data.get('tasks', []):
        task = {
            'name': task_data.get('name'),
            'description': task_data.get('description'),
            'expected_output': task_data.get('expected_output') or "Saída esperada não especificada.",
            'agent_id': task_data.get('agent_id'),
            'dependencies': task_data.get('dependencies', [])
        }
        created_task = create_task(task)
        created_tasks.append(created_task)

    return created_tasks


