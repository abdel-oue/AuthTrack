import logging

def write_log_file(datalist: list):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if function is called multiple times
    file_handler = logging.FileHandler("auth.log")
    formatter = logging.Formatter(fmt="%(asctime)s level=%(levelname)s service=auth user=%(user)s ip=%(ip)s status=%(status)s",datefmt="%Y-%m-%dT%H:%M:%S%z")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    for log_date, service, user, ip, status in datalist:
        extra = {"user": user, "ip": ip, "status": status}
        logger.info("", extra=extra)
