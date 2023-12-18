import argparse
import logging

from vibraniumdome_shields.settings_loader import settings

logging.basicConfig(level=settings.logger_level.DEFAULT_LOGGING_LEVEL)
for logger_name, log_level in settings.logger_level.to_dict().items():
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(prog='vibranium',
                                     description='Run security tests for the given LLM session',
                                     epilog='vibranium -s "{LLM Session}"')
    parser.add_argument("-s", "--session", help="LLM Session to test", required=True)


if __name__ == "__main__":
    main()
