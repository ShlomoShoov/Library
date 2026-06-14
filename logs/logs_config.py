import logging

logging.basicConfig(

    filename='logs/log.log'

)


def get_logger()->logging.logger:
    return logging.getLogger(__name__)
