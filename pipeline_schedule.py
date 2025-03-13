import sys
import json
import pytz
from google.cloud import aiplatform, storage
from datetime import datetime, timedelta

branch_name = sys.argv[1]
location = sys.argv[2]
project_number = sys.argv[3]
use_case_name = sys.argv[4]

aiplatform.init(location=location)
client = storage.Client()

bucket_name = ""
if branch_name == "sit":
    bucket_name = f"destination-test-promote-gcs"
elif branch_name == "uat":
    bucket_name = f"bkt-{use_case_name}-uat-mlops-dap"
elif branch_name == "production":
    bucket_name = f"bkt-{use_case_name}-prod-mlops-dap"
else:
    raise Exception(f"Error: Unsupported branch {branch_name}")

bucket = client.bucket(bucket_name)
blob = bucket.blob("pipeline/config.json")
content_config = json.dumps(blob.download_as_text())

SERVICE_ACCOUNT = f"{project_number}-compute@developer.gserviceaccount.com"

DISPLAY_NAME = content_config.get("pipeline_name")
PACKAGE_PATH = content_config.get("pipeline_package_path")
PIPELINE_ROOT = "gs://{}/pipeline_root".format(bucket_name)

job = aiplatform.PipelineJob(
    enable_caching=False,
    display_name=DISPLAY_NAME,
    template_path=PACKAGE_PATH,
    pipeline_root=PIPELINE_ROOT,
    parameter_values=content_config
)

job.create_schedule(
    cron="CRON_TZ=Asia/Jakarta 0 7 16 * *",
    display_name=f"{use_case_name}_scheduler", 
    service_account = SERVICE_ACCOUNT, 
)
