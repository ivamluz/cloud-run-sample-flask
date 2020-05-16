# cloud-run-sample-flask

## 1. Introduction

This project is a simple Flask app developed for helping to illustrate how to set up a deployment pipeline on GCP with Cloud Builder, Container Registry and Cloud Run.

Check the complete tutorial here. (**TODO:** Add link to article after publishing.)

## 2. Environment setup

### 2.1. Get the code

```bash
git clone git@github.com:ivamluz/cloud-run-sample-flask.git
cd cloud-run-sample-flask
```

### 2.2. Virtualenv

- Install Python 3.7+

- Create and activate an isolated Python environment

  ```bash
  virtualenv venv
  source ./venv/bin/activate
  ```

- Install the dependencies

  ```bash
  pip install --upgrade -r requirements.txt
  ```

## 3. Run the app locally

```bash
cd src

HASHED_API_KEY=`../scripts/hash_value.py --value "1234"` \
  gunicorn --bind :8080 --workers 1 --threads 8 app:app --reload
```

Here, `HASHED_API_KEY` is a variable used by the application to set up a basic auth mechanism. The intent of this is to show how to configure and use environment variables on Google Cloud Run.

## 4. Testing the app

From a different terminal instance, run the following command (notice the value for the `x-api-key` is the unhashed value passed to the `HASHED_API_KEY` variable in the previous command):

```bash
curl \
  -H'x-api-key: 1234' \
  'http://localhost:8080/hello'
```

**Expected Output**

```console
{"hello":"world"}
```

If you see the output above, it means everything is working as expected.

After everything is running, please make sure to keep reading the tutorial at (**TODO:** _LINK_TO_BE_ADDED_).

## 3. Prepare the application for deployment

### 3.1. Update the cloudbuild.yaml file

The versioned `cloudbuild.yaml` originally versioned in this repository has a placeholder for the Google Cloud Run service the application will be deployed with:

To set up it properly, make sure to follow these steps:

```bash
cd scripts/
chmod 755 setup.sh set_env_vars.sh

./setup.sh
```

When you run the `setup.sh` script, you will be prompted for the name your Google Cloud Run service should be deployed with.

For example, if `pipeline-demo` is entered, you are be expected to see an output similar to the following if you run `git diff` command:

```diff
diff --git a/cloudbuild.yaml b/cloudbuild.yaml
index 3998c9d..2881982 100644
--- a/cloudbuild.yaml
+++ b/cloudbuild.yaml
@@ -1,11 +1,11 @@
 steps:
   - name: gcr.io/cloud-builders/docker
     args:
-      ["build", "-t", "gcr.io/$PROJECT_ID/__SERVICE_NAME__:${SHORT_SHA}", "."]
+      ["build", "-t", "gcr.io/$PROJECT_ID/pipeline-demo:${SHORT_SHA}", "."]
     dir: "app"

   - name: "gcr.io/cloud-builders/docker"
-    args: ["push", "gcr.io/$PROJECT_ID/__SERVICE_NAME__"]
+    args: ["push", "gcr.io/$PROJECT_ID/pipeline-demo"]
     dir: "app"

   - name: "gcr.io/cloud-builders/gcloud"
@@ -14,9 +14,9 @@ steps:
         "beta",
         "run",
         "deploy",
-        "__SERVICE_NAME__",
+        "pipeline-demo",
         "--image",
-        "gcr.io/$PROJECT_ID/__SERVICE_NAME__:${SHORT_SHA}",
+        "gcr.io/$PROJECT_ID/pipeline-demo:${SHORT_SHA}",
         "--region",
         "us-central1",
         "--platform",
```

After the `cloudbuild.yaml`, make sure to commit and push your changes to the branch you want Google Cloud Build to watch for changes.
