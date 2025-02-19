### Import library untuk proses ###
from google.cloud import storage_transfer, aiplatform

### Import library untuk Service Account ###
from google.oauth2 import service_account
import json

client_storage_transfer = storage_transfer.StorageTransferServiceClient()
aiplatform.init(project="bdi-onprod", location="asia-southeast2")

### Definisi variabel ###

# Definisi project sumber dan tujuan serta masing-masing lokasi
source_project_id = "bdi-onprem"
source_location = "asia-southeast2"
destination_project_id = "bdi-onprod"
destination_location = "asia-southeast2"

# Definisi bucket GCS dari projek sumber dan projek tujuan
source_bucket = "source-test-promote-gcs"
destination_bucket = "destination-test-promote-gcs"

# Definisi Container Image untuk penggunaan library Scikit-Learn versi 1.3 dan XGBoost 1.7
CONTAINER_IMAGE_SKLEARN = "asia-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-3:latest"
CONTAINER_IMAGE_XGBOOST = "asia-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-7:latest"

def transfer_storage_promotion():
    transfer_job_name = ''

    request = storage_transfer.ListTransferJobsRequest(filter=f"{{'projectId':'{destination_project_id}'}}")
    page_result = client_storage_transfer.list_transfer_jobs(request=request)
    for x in page_result:
        if x.project_id == destination_project_id and x.transfer_spec.gcs_data_source.bucket_name == source_bucket and x.transfer_spec.gcs_data_sink.bucket_name == destination_bucket:
            transfer_job_name = x.name
            print(f"Found existing Storage Transfer Job : {transfer_job_name}")

    if transfer_job_name == '':
        print(f"Existing Storage Transfer Job Not Found. Creating New!")
        transfer_job_request = storage_transfer.CreateTransferJobRequest(
            {
                "transfer_job": {
                    "project_id": destination_project_id,
                    "description": "Transfer Data GCS Promotion Test",
                    "status": storage_transfer.TransferJob.Status.ENABLED,
                    "transfer_spec": {
                        "gcs_data_source": {
                            "bucket_name": source_bucket,
                        },
                        "gcs_data_sink": {
                            "bucket_name": destination_bucket,
                        },
                    },
                }
            }
        )

        result = client_storage_transfer.create_transfer_job(transfer_job_request)
        transfer_job_name = result.name
        print(f"Created Storage Transfer Job : {transfer_job_name}")

    print(f"Run Transfer Job : {transfer_job_name}")
    request = storage_transfer.RunTransferJobRequest(
        job_name=transfer_job_name,
        project_id=destination_project_id,
    )
    operation = client_storage_transfer.run_transfer_job(request=request)
    response = operation.result()

def import_model_registry_promotion():
    display_name = "casatocc_apply_any_card"
    models = aiplatform.Model.list(filter=f"display_name={display_name}")

    if len(models)>0:
        model_v1 = aiplatform.Model.upload(
            display_name=display_name,
            artifact_uri="gs://destination-test-promote-gcs/model-7893904149199192064/custom-trained/2025-02-17T06:29:17.926152Z",
            serving_container_image_uri=CONTAINER_IMAGE_SKLEARN,
            parent_model=models[0].resource_name,
            is_default_version=True,
        )
    else:
        model_v1 = aiplatform.Model.upload(
            display_name=display_name,
            artifact_uri="gs://destination-test-promote-gcs/model-7893904149199192064/custom-trained/2025-02-17T06:29:17.926152Z",
            serving_container_image_uri=CONTAINER_IMAGE_XGBOOST,
            is_default_version=True,
        )

def main():
    transfer_storage_promotion()
    import_model_registry_promotion()
        
if __name__ == '__main__':
    main()
