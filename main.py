from clause_classifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline 
from clause_classifier.logging import logger 

STAGE_NAME = 'data_ingestion_stage'
try:
    logger.info(f"stage {STAGE_NAME} started successfully")
    data_ingestion_pipeline = DataIngestionTrainingPipeline()
    data_ingestion_pipeline.main()
    logger.info(f"stage {STAGE_NAME} completed successfully")
except Exception as e:
    logger.exception(e)
    raise e
    
