# Data Model: Helm Chart for Todo Chatbot

## Overview
This document describes the data model for the Helm chart that will deploy the Todo Chatbot application. It defines the structure of the Kubernetes resources and configuration parameters.

## Helm Chart Metadata

### Chart.yaml
- **name**: todo-chatbot
- **version**: 0.1.0
- **appVersion**: "1.0"
- **description**: Helm chart for Todo Chatbot (React frontend + Python backend API)
- **type**: application
- **keywords**: 
  - todo
  - chatbot
  - react
  - python
  - ai
- **home**: ""
- **sources**: []
- **maintainers**: []
- **icon**: ""
- **apiVersion**: v2

## Configuration Values (values.yaml)

### Global Configuration
- **nameOverride**: string (default: "")
- **fullnameOverride**: string (default: "")

### Frontend Configuration
- **frontend.replicaCount**: integer (default: 2)
- **frontend.image.repository**: string (default: "todo-frontend")
- **frontend.image.pullPolicy**: string (default: "Always")
- **frontend.image.tag**: string (default: "latest")
- **frontend.service.type**: string (default: "LoadBalancer")
- **frontend.service.port**: integer (default: 80)
- **frontend.service.targetPort**: integer (default: 3000)
- **frontend.resources.limits.cpu**: string (default: "500m")
- **frontend.resources.limits.memory**: string (default: "512Mi")
- **frontend.resources.requests.cpu**: string (default: "100m")
- **frontend.resources.requests.memory**: string (default: "128Mi")
- **frontend.env.REACT_APP_BACKEND_URL**: string (default: "http://backend:8000")
- **frontend.probes.readiness.initialDelaySeconds**: integer (default: 20)
- **frontend.probes.readiness.periodSeconds**: integer (default: 10)
- **frontend.probes.liveness.initialDelaySeconds**: integer (default: 30)
- **frontend.probes.liveness.periodSeconds**: integer (default: 15)

### Backend Configuration
- **backend.replicaCount**: integer (default: 1)
- **backend.image.repository**: string (default: "todo-backend")
- **backend.image.pullPolicy**: string (default: "Always")
- **backend.image.tag**: string (default: "latest")
- **backend.service.type**: string (default: "ClusterIP")
- **backend.service.port**: integer (default: 8000)
- **backend.service.targetPort**: integer (default: 8000)
- **backend.resources.limits.cpu**: string (default: "1")
- **backend.resources.limits.memory**: string (default: "1Gi")
- **backend.resources.requests.cpu**: string (default: "200m")
- **backend.resources.requests.memory**: string (default: "256Mi")
- **backend.env.DATABASE_URL**: string (optional)
- **backend.env.SECRET_KEY**: string (optional)
- **backend.probes.readiness.initialDelaySeconds**: integer (default: 10)
- **backend.probes.readiness.periodSeconds**: integer (default: 5)
- **backend.probes.liveness.initialDelaySeconds**: integer (default: 20)
- **backend.probes.liveness.periodSeconds**: integer (default: 10)

### Security Configuration
- **securityContext.runAsNonRoot**: boolean (default: true)
- **securityContext.runAsUser**: integer (default: 1000)
- **securityContext.fsGroup**: integer (default: 2000)

## Kubernetes Resources

### Frontend Deployment
- **apiVersion**: apps/v1
- **kind**: Deployment
- **metadata.name**: {{ include "todo-chatbot.fullname" . }}-frontend
- **metadata.labels**: Standard app labels
- **spec.replicas**: {{ .Values.frontend.replicaCount }}
- **spec.selector.matchLabels**: App selector labels
- **spec.template.metadata.labels**: Pod labels
- **spec.template.spec.containers[]**:
  - name: frontend
  - image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}"
  - ports: [{ containerPort: 3000 }]
  - env: From values configuration
  - resources: From values configuration
  - readinessProbe: HTTP GET on /
  - livenessProbe: HTTP GET on /

### Backend Deployment
- **apiVersion**: apps/v1
- **kind**: Deployment
- **metadata.name**: {{ include "todo-chatbot.fullname" . }}-backend
- **metadata.labels**: Standard app labels
- **spec.replicas**: {{ .Values.backend.replicaCount }}
- **spec.selector.matchLabels**: App selector labels
- **spec.template.metadata.labels**: Pod labels
- **spec.template.spec.containers[]**:
  - name: backend
  - image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
  - ports: [{ containerPort: 8000 }]
  - env: From values configuration
  - resources: From values configuration
  - readinessProbe: HTTP GET on /health
  - livenessProbe: HTTP GET on /health

### Frontend Service
- **apiVersion**: v1
- **kind**: Service
- **metadata.name**: {{ include "todo-chatbot.fullname" . }}-frontend
- **metadata.labels**: Standard app labels
- **spec.type**: {{ .Values.frontend.service.type }}
- **spec.ports[]**:
  - port: {{ .Values.frontend.service.port }}
  - targetPort: {{ .Values.frontend.service.targetPort }}
- **spec.selector**: App selector labels

### Backend Service
- **apiVersion**: v1
- **kind**: Service
- **metadata.name**: {{ include "todo-chatbot.fullname" . }}-backend
- **metadata.labels**: Standard app labels
- **spec.type**: {{ .Values.backend.service.type }}
- **spec.ports[]**:
  - port: {{ .Values.backend.service.port }}
  - targetPort: {{ .Values.backend.service.targetPort }}
- **spec.selector**: App selector labels

### Helper Template (_helpers.tpl)
- **todo-chatbot.name**: Template for app name
- **todo-chatbot.fullname**: Template for full resource name
- **todo-chatbot.chart**: Template for chart name and version
- **todo-chatbot.labels**: Standard labels for resources
- **todo-chatbot.matchLabels**: Selector labels for deployments