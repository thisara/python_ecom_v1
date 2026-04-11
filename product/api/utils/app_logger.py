import logging

#read from config
c_log_level = logging.INFO
f_log_level = logging.INFO
f_file_path = '.'
f_file_name = "app.log"

def logger(module_name = __name__):
    log = logging.getLogger(module_name)
    log.setLevel(logging.DEBUG)

    if not log.handlers:

        console_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(stream_formatter)
        console_handler.setLevel(c_log_level)

        file_handler = logging.FileHandler(f_file_name)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(f_log_level)

        log.addHandler(console_handler)
        log.addHandler(file_handler)

    return log
