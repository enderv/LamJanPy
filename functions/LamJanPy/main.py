import logging
import yaml
from Janitor import Janitor

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    """
    Lambda handler
    """
    logger.info("%s - %s", event, context)

    with open("./config.yaml", 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    janitor_runner = Janitor(config)

    return event

if __name__ == '__main__':
    handle('test', 'test')
