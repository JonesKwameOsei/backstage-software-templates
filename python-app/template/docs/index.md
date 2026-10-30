# ${{ values.app_name }}

Welcome to the TechDocs home page for **${{ values.app_name }}**, a lightweight Flask REST API that reports the current server time and hostname. It is used as a sample service for exploring Kubernetes, Helm, Argo CD and Backstage.

!!! note
    This documentation is a placeholder. Sections marked _TBD_ will be expanded as the service evolves.

## Overview

| Property  | Value                                                                  |
| --------- | ----------------------------------------------------------------       |
| Type      | Service                                                                |
| Owner     | `${{ values.owner }}`                                                  |
| Lifecycle | `experimental`                                                         |
| Language  | Python 3.12 (Flask, Flask-RESTful)                                     |
| Port      | `5000`                                                                 |
| Source    | [GitHub](https://github.com/joneskwameosei-org/${{ values.app_name }}) |

## API Reference

### `GET /api/v1/info`

Returns the current time, the hostname of the pod serving the request, and a welcome message.

```json
{
  "time": "04:19:09PM on October 22, 2026",
  "hostname": "${{ values.app_name }}-7d9f8c6b5d-x2k4q",
  "message": "You are welcome to the ${{ values.app_name }}! 💝💖",
  "deployed_on": "kubernetes"
}
```

### `GET /`

Lists the service name, environment and available endpoints.

### `GET /livez`

Liveness probe. Returns `200` while the process can respond. It never checks dependencies,
so a database outage can't make Kubernetes restart every pod.

```json
{ "status": "alive" }
```

### `GET /readyz`

Readiness probe. Returns `200` when the pod can serve traffic. Add dependency checks here
(database, downstream APIs); a failing pod is removed from the Service until it recovers.

```json
{ "status": "ready" }
```

## Getting Started

### Run locally

```bash
pip install -r requirements.txt
python src/app.py
curl http://localhost:5000/api/v1/info
```

### Run with Docker

```bash
docker build -t ${{ values.app_name }} .
docker run -p 5000:5000 ${{ values.app_name }}
```

## Deployment

The service can be deployed to Kubernetes in several ways:

- **Raw manifests**: `deploy/` contains the Deployment, Service, Gateway, HTTPRoute and cert-manager resources.
- **Helm**: `charts/${{ values.app_name }}/` packages the app as a Helm chart.
- **Argo CD**: `argocd/${{ values.app_name }}.yaml` defines a GitOps Application that syncs the Helm chart using `argocd/values-argo.yaml`.

Traffic is routed through the Gateway API with TLS certificates issued by cert-manager.

## Repository Layout

```text
.
├── src/                 # Flask application source
├── charts/${{ values.app_name }}/   # Helm chart
├── deploy/              # Plain Kubernetes manifests
├── argocd/              # Argo CD Application and values
├── docs/                # TechDocs (this site)
├── Dockerfile
├── requirements.txt
└── catalog-info.yaml    # Backstage component definition
```

## Monitoring & Operations

_TBD_: dashboards, alerts and runbooks.

## Support

Questions or issues? Reach out to the **development** team or open an issue on the [GitHub repository](https://github.com/JonesKwameOsei/python-api/issues).
