# ${{ values.appName }}

${{ values.description }}

## Description

This is a Flask REST API application generated from the Flask API template.

## Features

- RESTful API endpoints
- Health check endpoint
- CORS support
- Docker support
- Environment-based configuration
- GitHub Actions CI/CD pipeline
- Google Cloud Build integration
- Kubernetes manifests for ArgoCD deployment

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

#### Development Mode

```bash
python app.py
```

The API will be available at `http://localhost:5000`

#### Production Mode (using Gunicorn)

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Environment Variables

- `FLASK_DEBUG`: Enable debug mode (default: False)
- `FLASK_HOST`: Host to bind to (default: 0.0.0.0)
- `FLASK_PORT`: Port to bind to (default: 5000)

### Docker

Build the Docker image:
```bash
docker build -t ${{ values.appName }} .
```

Run the container:
```bash
docker run -p 5000:5000 ${{ values.appName }}
```

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Items API
- `GET /api/v1/items` - Get all items
- `GET /api/v1/items/<id>` - Get a specific item
- `POST /api/v1/items` - Create a new item
- `PUT /api/v1/items/<id>` - Update an item
- `DELETE /api/v1/items/<id>` - Delete an item

## Example Requests

### Get all items
```bash
curl http://localhost:5000/api/v1/items
```

### Create an item
```bash
curl -X POST http://localhost:5000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{"name": "New Item", "description": "Item description"}'
```

### Get a specific item
```bash
curl http://localhost:5000/api/v1/items/1
```

## CI/CD

### GitHub Actions

This project includes two GitHub Actions workflows:

#### Build and Push (`build-push.yaml`)
- Runs tests on every push and PR
- Builds and pushes Docker image to Google Artifact Registry
- Triggered on pushes to `main` or `master` branches

#### Cloud Build (`cloudbuild.yaml` workflow)
- Submits build to Google Cloud Build
- Pushes image to Artifact Registry
- Updates Kubernetes manifests with new image tag

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `GCP_PROJECT_ID` | Your Google Cloud project ID |
| `GCP_SA_KEY` | Service account JSON key with Artifact Registry permissions |

### Google Cloud Build (Native)

You can also use Cloud Build directly with the included `cloudbuild.yaml`:

```bash
gcloud builds submit --config cloudbuild.yaml .
```

### Setting up GCP

1. Create an Artifact Registry repository:
```bash
gcloud artifacts repositories create ${{ values.appName }} \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for ${{ values.appName }}"
```

2. Create a service account for CI/CD:
```bash
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions"

gcloud projects add-iam-policy-binding ${{ values.gcpProjectId }} \
  --member="serviceAccount:github-actions@${{ values.gcpProjectId }}.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

## Kubernetes Deployment

Kubernetes manifests are located in the `manifests/` directory:
- `deployment.yaml` - Deployment with health probes
- `service.yaml` - ClusterIP service
- `kustomization.yaml` - Kustomize configuration

ArgoCD will automatically sync changes from the `manifests/` directory.

## License

Copyright (c) 2024

