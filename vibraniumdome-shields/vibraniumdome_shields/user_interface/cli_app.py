import argparse
import logging

from vibraniumdome_shields.settings_loader import settings

# from vibraniumdome_shields.vibranium_manager import VibraniumManager

# from pygments import lexers
# from pygments import highlight
# from pygments import formatters

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

    # args = parser.parse_args()
    # manager = VibraniumManager()
    # response = manager.default_scan(args.session)

    # print(
    #     highlight(
    #         response.model_dump_json(),
    #         lexers.JsonLexer(),
    #         formatters.TerminalFormatter()
    #     )
    # )


if __name__ == "__main__":
    main()
