import logging
from insurance.constant import *
import os
import pandas as pd

#from constant:
log_dir_path=LOG_DIR_PATH
log_file_path=LOG_FILE_PATH

#creating log dir:
os.makedirs(log_dir_path,exist_ok=True)

#logging:
logging.basicConfig(filename=log_file_path,
                    filemode="w",
                    format="[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s",
                    level=logging.INFO
                    )

def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    log_df.columns=columns
    
    log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

    return log_df[["log_message"]]
