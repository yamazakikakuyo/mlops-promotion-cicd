from google.cloud import aiplatform, storage
import json
import sys

branch_name = sys.argv[1]
model_display_name = sys.argv[2]
artifact_uri = sys.argv[3]
location = sys.argv[4]
project_id = sys.argv[5]

aiplatform.init(location="asia-southeast2")
client = storage.Client()

bucket_name = ""
if branch_name == "sit":
    bucket_name = "source-test-promote-gcs"
elif branch_name == "uat":
    bucket_name = "bkt-churn-uat-mlops-dap"
elif branch_name == "production":
    bucket_name = "bkt-churn-prod-mlops-dap"
else:
    raise Exception(f"Error: Unsupported branch {branch_name}") 

models = aiplatform.Model.list(order_by="update_time desc")

parent_model = None
for model in models:
    if model.display_name.lower() == model_display_name.lower():
        parent_model = model
        break

file = ""
blobs = list(client.list_blobs(bucket_name, prefix=artifact_uri))
if len(blobs) > 0:
    blobs = list(set(["/".join(blob.name.split('/')[:4]) for blob in blobs]))
    model_folder = sorted(blobs, reverse=True)[0]
else:
    raise Exception(f"Error: no model that is stored") 

bucket = client.bucket("bkt-churn-dev-mlops-dap")
blob = bucket.blob(model_folder+"/environment.json")
content = blob.download_as_text()
container_uri = json.loads(content).get("container_uri")

test_model = aiplatform.Model.upload(
    display_name="churn",
    artifact_uri=f"gs://{bucket_name}/{model_folder}",
    serving_container_image_uri=container_uri,
    instance_schema_uri=f"gs://{bucket_name}/{model_folder}/prediction_schema.yaml",
    prediction_schema_uri=f"gs://{bucket_name}/{model_folder}/instance.yaml",
    parent_model=parent_model.resource_name,
    is_default_version=True,
    sync=True,
)
