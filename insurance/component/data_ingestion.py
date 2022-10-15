from insurance.entity.artifact_entity import DataIngestionArtifact
from insurance.logger import logging
from insurance.exception import InsuranceException
from insurance.entity.config_entity import DataIngestionConfig
from sklearn.model_selection import StratifiedShuffleSplit
import os
import sys
from six.moves import urllib
import tarfile
import pandas as pd
import numpy as np


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig) -> None:
        try:
            logging.info(f"{'>>'*20} Data Ingestion Started{'>>'*20}")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def download_insurance_data(self)->str:
        try:
            #download url
            download_url=self.data_ingestion_config.dataset_download_url

            #dowload location for tgz file
            tgz_download_dir=self.data_ingestion_config.tgz_download_dir

            #creating dir
            os.makedirs(tgz_download_dir,exist_ok=True)

            #dataset file name
            insurance_file_name=os.path.basename(download_url)

            #dataset file path
            tgz_file_path=os.path.join(tgz_download_dir,insurance_file_name)

            #downloading
            logging.info(f"downloading file from url: {download_url} into file: {tgz_file_path}")
            urllib.request.urlretrieve(download_url,tgz_file_path)

            logging.info(f"file: {tgz_file_path} has been downloaded successfully")
            return tgz_file_path
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            #create dir:
            os.makedirs(raw_data_dir,exist_ok=True)

            #extracting file:
            logging.info(f"Extracting tgz file from: {tgz_file_path} to: {raw_data_dir}")
            with tarfile.open(tgz_file_path) as tgz_file_object:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tgz_file_object, path=raw_data_dir)

            logging.info(f"Extraction completed")
            
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir
            
            file_name=os.listdir(raw_data_dir)[0]

            #dataset file path:
            insurance_file_path=os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv file path:{insurance_file_path}")
            insurance_data_frame=pd.read_csv(insurance_file_path)

            #adding one column and using pd.cut
            insurance_data_frame['expense_cat']=pd.cut(insurance_data_frame['expenses'],
                                                        bins=[0.0,1.5,3.0,4.5,6,np.inf],
                                                        labels=[1,2,3,4,5]
                                                        )
            logging.info(f"splitting data into train set and test set using stratified shuffle split")
            strat_train_set=None
            strat_test_set=None

            split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)

            for train_index, test_index in split.split(insurance_data_frame,insurance_data_frame['expense_cat']):
                strat_train_set=insurance_data_frame.loc[train_index].drop(['expense_cat'],axis=1)
                strat_test_set=insurance_data_frame.loc[test_index].drop(['expense_cat'],axis=1)

            #set file path:
            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            #creating train_dir and exporting to csv
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training data to file: {train_file_path}")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Exporting testing data to file: {test_file_path}")
                strat_test_set.to_csv(test_file_path,index=False)

            data_ingestion_artifact=DataIngestionArtifact(train_file_path=train_file_path,
                                                        test_file_path=test_file_path,
                                                        is_ingested=True,
                                                        message=f"Data Ingestion Completed successfully"
                                                        )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            tgz_file_path=self.download_insurance_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise InsuranceException(e,sys) from e 

    def __del__(self):
        logging.info(f"{'>>'*20} Data Ingestion Ended{'>>'*20}")