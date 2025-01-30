from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.pipeline.data_transform_pipeline import DataTransformPipeline

if __name__=="__main__":
    #pipelineING=DataIngestionPipeline()
    #pipelineING.run()

    pipelineTra=DataTransformPipeline()
    pipelineTra.run()

