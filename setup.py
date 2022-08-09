from setuptools import setup, find_packages
from typing import List
import os

PROJECT_NAME="insurance"
PROJECT_DESCRIPTION="ml-premium-prediction-regression-model"
PROJECT_VERSION="0.0.1"
AUTHOR="Manish Prabhat"
REQUIREMENT_FILE="requirements.txt"

HYPHEN_E_DOT="-e ."

def get_requirement_list()->List[str]:
    with open(REQUIREMENT_FILE,"r") as requirement_file:
        requirement_list=requirement_file.readlines()
        requirement_list=[requirement_name.replace("\n","") for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list=requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list


setup(
    name=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=PROJECT_VERSION,
    author=AUTHOR,
    packages=find_packages(),
    install_requires=get_requirement_list()
)
