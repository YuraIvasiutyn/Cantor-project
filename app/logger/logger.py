import logging

logging.basicConfig(
    level='INFO', filename='log.log', format="%(asctime)s %(levelname)s\t%(filename)s\t%(funcName)s: %(message)s")
logger = logging.getLogger()


def main(name):
    logger.info(f'Argument {name}')


if __name__ == '__main__':
    main('Yurii')
