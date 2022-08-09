import os
from datetime import datetime

def get_current_time_stamp()->str:
    c_time_stamp=f"{datetime.now().strftime('%y-%m-%d-%H-%M-%S')}"
    return c_time_stamp
    
#root Dir , Project Dir & current time stamp 
ROOT_DIR=os.getcwd()
CURRENT_TIME_STAMP = get_current_time_stamp()

#logger constant
LOG_DIR="logs"
LOG_FILE_NAME=f"log_{CURRENT_TIME_STAMP}.log"
LOG_DIR_PATH=os.path.join(ROOT_DIR,LOG_DIR)
LOG_FILE_PATH=os.path.join(LOG_DIR_PATH,LOG_FILE_NAME)

#Config file:
CONFIG_FILE_DIR_NAME="config"
CONFIG_FILE_NAME="config.yaml"
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_FILE_DIR_NAME,CONFIG_FILE_NAME)

#variables related to trainingpipeline

TRAINING_PIPELINE_CONFIG_KEY="training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY="pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY="artifact_dir"

#variable related to Data Ingestion:

DATA_INGESTION_CONFIG_KEY="data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR="data_ingestion"
DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY="dataset_download_url"
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY="tgz_download_dir"
DATA_INGESTION_RAW_DATA_DIR_KEY="raw_data_dir"
DATA_INGESTION_INGESTED_DATA_DIR_KEY="ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY="ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DIR_KEY="ingested_test_dir"

#variable related to Data Validation:
DATA_VALIDATION_CONFIG_KEY="data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR="data_validation"
DATA_VALIDATION_SCHEMA_DIR_KEY="schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY="schema_file_name"
DATA_VALIDATION_REPORT_FILE_NAME_KEY="report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY="report_page_file_name"

#variable related to Data Transformation:
DATA_TRANSFORMATION_CONFIG_KEY="data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY="transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY="transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY="transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSED_DIR_KEY="preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_KEY="preprocessed_object_file_name"


#variable related to schema file:
SCHEMA_FILE_COLUMNS_KEY="columns"
SCHEMA_FILE_COLUMNS_COUNT_KEY="number_of_columns"
SCHEMA_FILE_CATEGORICAL_COLUMNS_KEY="categorical_columns"
SCHEMA_FILE_NUMERICAL_COLUMNS_KEY="numerical_columns"
SCHEMA_FILE_TARGET_COLUMNS_KEY="target_column"
SCHEMA_FILE_DOMAIN_VALUE_KEY="domain_value"
SCHEMA_FILE_DOMAIN_VALUE_SEX_KEY="sex"
SCHEMA_FILE_DOMAIN_VALUE_SMOKER_KEY="smoker"
SCHEMA_FILE_DOMAIN_VALUE_REGiON_KEY="region"

#model trainer related varibles:

MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
MODEL_TRAINER_CONFIG_KEY="model_trainer_config"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY="trained_model_dir"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY="model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY="base_accuracy"
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY="model_config_dir"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY="model_config_file_name"

#Model evaluation:
MODEL_EVALUATION_CONFIG_KEY="model_evaluation_config"
MODEL_EVALUATION_FILE_NAME_KEY="model_evaluation_file_name"
MODEL_EVALUATION_ARTIFACT_DIR="model_evaluation"

#Model Pusher Config key
MODEL_PUSHER_CONFIG_KEY="model_pusher_config"
MODEL_PUSHER_MODEL_EXPORT_DIR_KEY="model_export_dir"

BEST_MODEL_KEY="best_model"
HISTORY_KEY="history"
MODEL_PATH_KEY="model_path"

EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"