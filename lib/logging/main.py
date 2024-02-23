import logging

def configure_logger():
    # Configure the root logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("./log/application.log"),
                            logging.StreamHandler()
                        ])
