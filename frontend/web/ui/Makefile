include .env

deploy:
	gcloud run deploy ${SERVICE_NAME} \
		--project=${GOOGLE_CLOUD_PROJECT} \
		--region=asia-southeast1 \
		--set-env-vars="BACKEND_HOST=${BACKEND_HOST}" \
		--source=.
