include .env

deploy:
	gcloud run deploy ${SERVICE_NAME} \
		--project=${GOOGLE_CLOUD_PROJECT}
		--region=asia-southeast1 \
		--source=.

run:
	uvicorn app.main:app --reload
