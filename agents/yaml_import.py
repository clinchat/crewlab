import yaml
from agent_manager import create_agent


def import_agents_from_yaml(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    created_agents = []
    for agent_data in data.get('agents', []):
        agent = {
            'agent_id': agent_data.get('id'),
            'name': agent_data.get('id'),  # Pode ajustar conforme desejado
            'role': agent_data.get('role'),
            'goal': agent_data.get('goal'),
            'backstory': agent_data.get('backstory'),
            'verbose': agent_data.get('verbose', True),
            'allow_delegation': agent_data.get('allow_delegation', False),
            'memory': agent_data.get('memory', False),
            'tools': agent_data.get('tools', []),
            'llm_config': agent_data.get('llm', {})
        }
        created_agent = create_agent(agent)
        created_agents.append(created_agent)

    return created_agents
