import logging

def write_log_file(datalist : list):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # file handler
    file_handler = logging.FileHandler("auth.log")
    formatter = logging.Formatter(fmt="%(asctime)s level=%(levelname)s service=auth user=%(user)s ip=%(ip)s", datefmt="%Y-%m-%dT%H:%M:%S%z")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    for date, attempt, session, user, ip in datalist:
        extra = {"user": user, "ip": ip}
        logger.info("", extra=extra)