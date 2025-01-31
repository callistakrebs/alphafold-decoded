import yaml

def convert_yaml_to_requirements(yaml_file, output_file='requirements.txt'):
    """
    Convert a YAML environment file to requirements.txt format.
    
    Args:
        yaml_file (str): Path to the input YAML file
        output_file (str): Path to the output requirements.txt file
    """
    with open(yaml_file, 'r') as f:
        yaml_data = yaml.safe_load(f)
    
    # Extract dependencies based on common YAML environment file formats
    dependencies = []
    
    # Handle different YAML structure possibilities
    if 'dependencies' in yaml_data:
        for dep in yaml_data['dependencies']:
            if isinstance(dep, str) and not dep.startswith('python'):
                # Remove any version spaces and replace == with =
                dep = dep.replace(' ', '')
                dependencies.append(dep)
    elif 'packages' in yaml_data:
        for dep in yaml_data['packages']:
            if isinstance(dep, str):
                dependencies.append(dep)
    
    # Write to requirements.txt
    with open(output_file, 'w') as f:
        for dep in dependencies:
            f.write(f"{dep}\n")

if __name__ == "__main__":
    # Example usage
    convert_yaml_to_requirements('environment_mac.yml')