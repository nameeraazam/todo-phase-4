# Todo Chatbot Helm Chart

This Helm chart deploys the Todo Chatbot application, which consists of a React frontend and a Python backend API.

## Prerequisites

- Kubernetes 1.20+
- Helm 3.0+

## Installing the Chart

To install the chart with the release name `todo-chatbot`:

```bash
helm install todo-chatbot ./helm-chart --namespace todo-app --create-namespace
```

## Configuration

The following tables lists the configurable parameters of the todo-chatbot chart and their default values.

### Frontend Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `frontend.replicaCount` | Number of frontend pods to run | `2` |
| `frontend.image.repository` | Frontend image repository | `todo-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `Always` |
| `frontend.service.type` | Frontend service type | `LoadBalancer` |
| `frontend.service.port` | Frontend service port | `80` |
| `frontend.service.targetPort` | Frontend service target port | `3000` |
| `frontend.resources.limits.cpu` | Frontend CPU limit | `500m` |
| `frontend.resources.limits.memory` | Frontend memory limit | `512Mi` |
| `frontend.resources.requests.cpu` | Frontend CPU request | `100m` |
| `frontend.resources.requests.memory` | Frontend memory request | `128Mi` |
| `frontend.env.REACT_APP_BACKEND_URL` | Backend URL for frontend | `http://backend:8000` |

### Backend Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `backend.replicaCount` | Number of backend pods to run | `1` |
| `backend.image.repository` | Backend image repository | `todo-backend` |
| `backend.image.tag` | Backend image tag | `latest` |
| `backend.image.pullPolicy` | Backend image pull policy | `Always` |
| `backend.service.type` | Backend service type | `ClusterIP` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.service.targetPort` | Backend service target port | `8000` |
| `backend.resources.limits.cpu` | Backend CPU limit | `1` |
| `backend.resources.limits.memory` | Backend memory limit | `1Gi` |
| `backend.resources.requests.cpu` | Backend CPU request | `200m` |
| `backend.resources.requests.memory` | Backend memory request | `256Mi` |

### Security Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `securityContext.runAsNonRoot` | Run containers as non-root user | `true` |
| `securityContext.runAsUser` | UID to run containers as | `1000` |
| `securityContext.fsGroup` | GID for shared volumes | `2000` |

## Customizing Values

You can customize the deployment by creating a custom values file:

```yaml
frontend:
  replicaCount: 3
  image:
    repository: my-registry/todo-frontend
    tag: v1.0.0
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 700m
      memory: 768Mi

backend:
  replicaCount: 2
  image:
    repository: my-registry/todo-backend
    tag: v1.0.0
  resources:
    requests:
      cpu: 300m
      memory: 384Mi
    limits:
      cpu: 1.2
      memory: 1.2Gi
```

Then install with:

```bash
helm install todo-chatbot ./helm-chart -f custom-values.yaml --namespace todo-app --create-namespace
```

## Uninstalling the Chart

To uninstall/delete the `todo-chatbot` release:

```bash
helm uninstall todo-chatbot --namespace todo-app
```

## Chart Structure

- `Chart.yaml`: Contains chart metadata
- `values.yaml`: Default configuration values
- `templates/`: Kubernetes manifest templates
  - `deployment-frontend.yaml`: Frontend deployment template
  - `deployment-backend.yaml`: Backend deployment template
  - `service-frontend.yaml`: Frontend service template
  - `service-backend.yaml`: Backend service template
  - `_helpers.tpl`: Common template helpers