import os
from box.exceptions import BoxError, BoxKeyError, BoxTypeError, BoxValueError, BoxWarning
import yaml
from clause_classifier.logging import logger
from ensure import ensure_annotations
from box import ConfigBox  # use to access dictionary type values using . operator 
from pathlib import Path
from typing import Any 

@ensure_annotations
def read_yaml(path_to_yaml:Path)-> ConfigBox:
    """read yaml file and returns 
    
    Args:
        path_to_yaml (str): path like input 

    Raises: 
        ValueError: if yaml file is empty 
        e: empty file 
    Returns:
        ConfigBox: ConfigBox type    
        """
    try:
        with open(path_to_yaml, 'r') as f:
            yaml_data = yaml.safe_load(f)
            if yaml_data is None:
                raise ValueError("yaml file is empty")
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            config_box = ConfigBox(yaml_data)
            return config_box
    except (FileNotFoundError, BoxError, BoxKeyError, BoxTypeError, BoxValueError, BoxWarning) as e:
        logger.error(f"Error reading yaml file: {path_to_yaml}, {e}")
        raise e


@ensure_annotations
def create_directories(path_to_directories:list, verbose=True):
    """create directories if they don't exist
    
    Args:
        path_to_directories (list[str]): list of paths like input 
        verbose (bool, optional): verbosity flag. Defaults to True.
        ignore_log(bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory: {path}")

@ensure_annotations
def get_size(path:Path) -> str: # here return type shoudl be a string 
    """get size of file in bytes
    
    Args:
        path (str): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"
