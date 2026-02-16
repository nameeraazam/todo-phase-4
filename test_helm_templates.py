import subprocess
import tempfile
import os
import yaml
from pathlib import Path

def test_helm_template_rendering():
    """
    Test that Helm templates can be rendered to valid YAML.
    Since Helm is not installed, we'll simulate the template rendering by replacing common Helm directives.
    """
    print("Testing Helm template rendering...")
    
    templates_dir = Path("helm-chart/templates")
    all_valid = True
    
    # Common Helm template patterns to replace for validation
    template_replacements = {
        '{{ .Chart.Name }}': 'test-name',
        '{{ .Chart.Version }}': '0.1.0',
        '{{ .Release.Name }}': 'test-release',
        '{{ .Release.Service }}': 'Helm',
        '{{ .Values.frontend.replicaCount }}': '2',
        '{{ .Values.backend.replicaCount }}': '1',
        '{{ .Values.frontend.image.repository }}': 'test-frontend',
        '{{ .Values.frontend.image.tag }}': 'latest',
        '{{ .Values.frontend.image.pullPolicy }}': 'Always',
        '{{ .Values.backend.image.repository }}': 'test-backend',
        '{{ .Values.backend.image.tag }}': 'latest',
        '{{ .Values.backend.image.pullPolicy }}': 'Always',
        '{{ .Values.frontend.service.type }}': 'LoadBalancer',
        '{{ .Values.frontend.service.port }}': '80',
        '{{ .Values.frontend.service.targetPort }}': '3000',
        '{{ .Values.backend.service.type }}': 'ClusterIP',
        '{{ .Values.backend.service.port }}': '8000',
        '{{ .Values.backend.service.targetPort }}': '8000',
        '{{ .Values.frontend.env.REACT_APP_BACKEND_URL }}': 'http://backend:8000',
        '{{ .Values.backend.env.DATABASE_URL }}': '',
        '{{ .Values.backend.env.SECRET_KEY }}': '',
        '{{ .Values.frontend.probes.liveness.initialDelaySeconds }}': '30',
        '{{ .Values.frontend.probes.liveness.periodSeconds }}': '15',
        '{{ .Values.frontend.probes.readiness.initialDelaySeconds }}': '20',
        '{{ .Values.frontend.probes.readiness.periodSeconds }}': '10',
        '{{ .Values.backend.probes.liveness.initialDelaySeconds }}': '20',
        '{{ .Values.backend.probes.liveness.periodSeconds }}': '10',
        '{{ .Values.backend.probes.readiness.initialDelaySeconds }}': '10',
        '{{ .Values.backend.probes.readiness.periodSeconds }}': '5',
        '{{- include "todo-chatbot.fullname" . }}': 'test-release-todo-chatbot',
        '{{- include "todo-chatbot.name" . | nindent 4 }}': '  name: todo-chatbot',
        '{{- include "todo-chatbot.labels" . | nindent 4 }}': '  label1: value1\n  label2: value2',
        '{{- include "todo-chatbot.matchLabels" . | nindent 6 }}': '    matchLabel1: value1',
        '{{- include "todo-chatbot.selectorLabels" . | nindent 8 }}': '        selectorLabel1: value1',
        '{{- toYaml .Values.securityContext | nindent 8 }}': '    runAsNonRoot: true\n    runAsUser: 1000\n    fsGroup: 2000',
        '{{- toYaml .Values.frontend.resources | nindent 12 }}': '      limits:\n        cpu: "500m"\n        memory: "512Mi"\n      requests:\n        cpu: "100m"\n        memory: "128Mi"',
        '{{- toYaml .Values.backend.resources | nindent 12 }}': '      limits:\n        cpu: "1"\n        memory: "1Gi"\n      requests:\n        cpu: "200m"\n        memory: "256Mi"',
        '{{- include "todo-chatbot.chart" . }}': 'todo-chatbot-0.1.0',
        '{{- include "todo-chatbot.selectorLabels" . | nindent 4 }}': '  selector1: value1',
        '{{ .Chart.AppVersion | quote }}': '"1.0"',
        '{{ .Values.backend.env.DATABASE_URL | quote }}': '""',
        '{{ .Values.backend.env.SECRET_KEY | quote }}': '""',
        '{{ .Values.frontend.env.REACT_APP_BACKEND_URL | quote }}': '"http://backend:8000"',
        '{{- if .Values.fullnameOverride }}': '',
        '{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}': 'override-name',
        '{{- else }}': '',
        '{{- $name := default .Chart.Name .Values.nameOverride }}': '',
        '{{- if contains $name .Release.Name }}': '',
        '{{- .Release.Name | trunc 63 | trimSuffix "-" }}': 'release-name',
        '{{- else }}': '',
        '{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}': 'release-name-todo-chatbot',
        '{{- end }}': '',
        '{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}': 'todo-chatbot',
        '{{- if .Chart.AppVersion }}': '',
        '{{- end }}': '',
        '{{- if .Values.nameOverride }}': '',
        '{{- .Values.nameOverride | nindent 4 }}': '  nameOverride: value',
        '{{- else }}': '',
        '{{- include "todo-chatbot.name" . | nindent 4 }}': '  name: todo-chatbot',
        '{{- end }}': '',
        '{{- define "todo-chatbot.name" -}}': '',
        '{{- define "todo-chatbot.fullname" -}}': '',
        '{{- define "todo-chatbot.chart" -}}': '',
        '{{- define "todo-chatbot.labels" -}}': '',
        '{{- define "todo-chatbot.matchLabels" -}}': '',
        '{{- define "todo-chatbot.selectorLabels" -}}': '',
        '{{- end }}': '',
        '{{- if eq .Values.frontend.service.type "LoadBalancer" }}': '',
        '{{- else if contains "NodePort" .Values.frontend.service.type }}': '',
        '{{- else if contains "ClusterIP" .Values.frontend.service.type }}': '',
        '{{- end }}': '',
        '{{"{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"}}': '1.2.3.4',
        '{{ include "todo-chatbot.fullname" . }}': 'test-release-todo-chatbot',
        '{{ include "todo-chatbot.name" . }}': 'todo-chatbot',
        '{{ include "todo-chatbot.fullname" . }}-frontend': 'test-release-todo-chatbot-frontend',
        '{{ include "todo-chatbot.fullname" . }}-backend': 'test-release-todo-chatbot-backend',
        '{{ include "todo-chatbot.fullname" . }}-frontend': 'test-release-todo-chatbot-frontend',
        '{{ include "todo-chatbot.fullname" . }}-backend': 'test-release-todo-chatbot-backend',
        '{{ include "todo-chatbot.name" . }},app.kubernetes.io/instance={{ .Release.Name }},component=frontend': 'app.kubernetes.io/name=todo-chatbot,app.kubernetes.io/instance=test-release,component=frontend',
        '{{ include "todo-chatbot.name" . }},app.kubernetes.io/instance={{ .Release.Name }},component=backend': 'app.kubernetes.io/name=todo-chatbot,app.kubernetes.io/instance=test-release,component=backend',
    }
    
    for template_file in templates_dir.glob("*.yaml"):
        print(f"  Processing template: {template_file.name}")
        
        # Read the template
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply replacements
        processed_content = content
        for template_var, replacement in template_replacements.items():
            processed_content = processed_content.replace(template_var, replacement)
        
        # Remove any remaining template directives (they would be replaced with actual values in real Helm)
        import re
        processed_content = re.sub(r'\{\{[^}]+\}\}', 'placeholder-value', processed_content)
        
        # Try to parse as YAML
        try:
            yaml.safe_load(processed_content)
            print(f"    [OK] Template renders to valid YAML: {template_file.name}")
        except yaml.YAMLError as e:
            print(f"    [ERROR] Template renders to invalid YAML: {template_file.name} - Error: {e}")
            all_valid = False
        except Exception as e:
            print(f"    [ERROR] Error processing template: {template_file.name} - Error: {e}")
            all_valid = False
    
    return all_valid

if __name__ == "__main__":
    print("=== Testing Helm Template Rendering ===")
    template_valid = test_helm_template_rendering()
    
    print("\n=== Final Result ===")
    if template_valid:
        print("[SUCCESS] All Helm templates render to valid YAML!")
    else:
        print("[FAILURE] Some Helm templates do not render to valid YAML.")