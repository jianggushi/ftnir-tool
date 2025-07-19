import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.debug("这是一条 DEBUG 日志，会写到 app_debug.log")
    logger.info("这是一条 INFO 日志，会打印到控制台")
    logger.error("这是一条 ERROR 日志，会额外写到 app_error.log")
