from google.cloud import aiplatform, storage
import sys
print(sys.argv)
# if len(sys.argv) > 1:
#     print("First argument:", sys.argv[1])
# else:
#     print("No argument provided.")

# aiplatform.init(location="asia-southeast2")

# test_model = aiplatform.Model.upload(
#     display_name="churn",
#     artifact_uri="gs://bkt-churn-dev-mlops-dap/model/model-2287309641215901696/tf-saved-model/2025-03-07T12:51:48.227643Z/",
#     serving_container_image_uri="asia-docker.pkg.dev/vertex-ai/automl-tabular/prediction-server:20250218_0625",
#     instance_schema_uri="gs://bkt-churn-dev-mlops-dap/model/model-2287309641215901696/tf-saved-model/2025-03-07T12:51:48.227643Z/prediction_schema.yaml",
#     prediction_schema_uri="gs://bkt-churn-dev-mlops-dap/model/model-2287309641215901696/tf-saved-model/2025-03-07T12:51:48.227643Z/instance.yaml",
#     parent_model="projects/prj-273fa85c8fac49df/locations/asia-southeast2/models/2287309641215901696",
#     is_default_version=True,
#     sync=True,
# )
