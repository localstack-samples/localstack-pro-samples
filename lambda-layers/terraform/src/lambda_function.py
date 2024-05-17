import yaml

def handler(event, context):
    status_yaml = """
    status: success
    """
    status = yaml.safe_load(status_yaml)
    return status
