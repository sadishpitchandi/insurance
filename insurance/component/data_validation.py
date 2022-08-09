from cmath import log

from evidently import dashboard
from insurance.constant import SCHEMA_FILE_COLUMNS_COUNT_KEY, SCHEMA_FILE_COLUMNS_KEY, SCHEMA_FILE_DOMAIN_VALUE_KEY, SCHEMA_FILE_DOMAIN_VALUE_SEX_KEY, TRAINING_PIPELINE_ARTIFACT_DIR_KEY
from insurance.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from insurance.config.configuration import DataValidationConfig
from insurance.logger import logging
from insurance.exception import InsuranceException
from insurance.util.util import read_yaml_file
import pandas as pd
import numpy as np
import os,sys
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json



class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact) -> None:
        try:
            logging.info(f"{'>>'*30}Data Valdaition log started.{'<<'*30} \n\n")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_train_and_test_df(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist=False
            is_test_file_exist=False

            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            #checking for file existance
            is_train_file_exist=os.path.exists(train_file_path)
            is_test_file_exist=os.path.exists(test_file_path)

            is_available=is_train_file_exist and is_test_file_exist

            logging.info(f"is train & test file exists -> {is_available}")

            if not is_available:
                training_file=self.data_ingestion_artifact.train_file_path
                testing_file=self.data_ingestion_artifact.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file}" \
                        "is not present"
                raise Exception(message)
            return is_available
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def validate_dataset_schema(self)->bool:
        try:
            logging.info("Checking if Number of columns, column names & domain values are correct")
            validation_status=False
            train_df,test_df=self.get_train_and_test_df()
            list_df=[train_df,test_df]
            schema_file_path=self.data_validation_config.schema_file_path
            schema_file_config=read_yaml_file(schema_file_path)

            #validating number of columns in train & test data
            check_num_of_columns=False
            if len(train_df.columns)==schema_file_config[SCHEMA_FILE_COLUMNS_COUNT_KEY] and \
                len(test_df.columns)==schema_file_config[SCHEMA_FILE_COLUMNS_COUNT_KEY]:
                check_num_of_columns=True
            
            #validating column names in train & test data:
            check_col_names=False
            for col_names in  schema_file_config[SCHEMA_FILE_COLUMNS_KEY]:
                if col_names in train_df.columns and \
                    col_names in test_df.columns:
                    check_col_names=True
                else:
                    check_col_names=False
                    break
            
            #checking domain values of columns sex, smoker, region:
            check_domain_value=False
            domain_values=schema_file_config[SCHEMA_FILE_DOMAIN_VALUE_KEY]
            for df in list_df:
                if check_domain_value==False:
                        break
                else:
                    for column in domain_values:
                        if check_domain_value==False:
                            break
                        else:
                            for element in df[column]:
                                if element in domain_values[element]:
                                    check_domain_value=True
                                else:
                                    check_domain_value=False
                                    break
            validation_status=check_num_of_columns & check_col_names & check_domain_value
            logging.info(f"Validation Status Number of columns:=>[{check_num_of_columns}] Column Names:=> \
                        [{check_col_names}] and domain values:=> [{check_domain_value}]")
            return validation_status
        except Exception as e:
            raise InsuranceException(e,sys) from e
    
    def get_and_save_data_drift_report(self):
        try:
            profile=Profile(sections=[DataDriftProfileSection()])
            train_df,test_df=self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report=json.loads(profile.json())

            report_file_path=self.data_validation_config.report_file_path
            report_dir=os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,'w') as report_file:
                json.dump(report,report_file,indent=6)
            return report

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard=Dashboard(tabs=[DataDriftTab()])
            train_df,test_df=self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path=self.data_validation_config.report_page_file_path
            report_page_dir=os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report=self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact=DataValidationArtifact(
                                    schema_file_path=self.data_validation_config.schema_file_path,
                                    report_file_path=self.data_validation_config.report_file_path,
                                    report_page_file_path=self.data_validation_config.report_page_file_path,
                                    is_validated=True,
                                    message="Data Validation performed successfully"
                                    )
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*30}Data Valdaition log completed.{'<<'*30} \n\n")