import os
from pathlib import Path

def check_template_structure():
    """Check that templates have the expected structure."""
    templates_dir = Path("helm-chart/templates")
    all_valid = True
    
    # Expected elements in each template
    expected_elements = {
        "deployment-frontend.yaml": [
            "apiVersion: apps/v1",
            "kind: Deployment",
            "{{ include \"todo-chatbot.fullname\" . }}-frontend",
            "{{ .Values.frontend.replicaCount }}",
            "containerPort: 3000",
            "{{ .Values.frontend.image.repository }}",
            "{{ .Values.frontend.image.tag }}"
        ],
        "deployment-backend.yaml": [
            "apiVersion: apps/v1",
            "kind: Deployment",
            "{{ include \"todo-chatbot.fullname\" . }}-backend",
            "{{ .Values.backend.replicaCount }}",
            "containerPort: 8000",
            "{{ .Values.backend.image.repository }}",
            "{{ .Values.backend.image.tag }}",
            "/health"
        ],
        "service-frontend.yaml": [
            "apiVersion: v1",
            "kind: Service",
            "{{ include \"todo-chatbot.fullname\" . }}-frontend",
            "{{ .Values.frontend.service.type }}",
            "port: {{ .Values.frontend.service.port }}",
            "targetPort: {{ .Values.frontend.service.targetPort }}"
        ],
        "service-backend.yaml": [
            "apiVersion: v1",
            "kind: Service",
            "{{ include \"todo-chatbot.fullname\" . }}-backend",
            "{{ .Values.backend.service.type }}",
            "port: {{ .Values.backend.service.port }}",
            "targetPort: {{ .Values.backend.service.targetPort }}"
        ],
        "_helpers.tpl": [
            "{{- define \"todo-chatbot.name\" -}}",
            "{{- define \"todo-chatbot.fullname\" -}}",
            "{{- define \"todo-chatbot.labels\" -}}"
        ]
    }
    
    for template_name, elements in expected_elements.items():
        template_path = templates_dir / template_name
        if not template_path.exists():
            print(f"[ERROR] Template file missing: {template_name}")
            all_valid = False
            continue
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Checking template: {template_name}")
        for element in elements:
            if element in content:
                print(f"  [OK] Found: {element[:50]}{'...' if len(element) > 50 else ''}")
            else:
                print(f"  [MISSING] {element[:50]}{'...' if len(element) > 50 else ''}")
                all_valid = False
    
    return all_valid

def check_values_and_chart():
    """Check that Chart.yaml and values.yaml have expected content."""
    print("\nChecking Chart.yaml...")
    chart_path = Path("helm-chart/Chart.yaml")
    if chart_path.exists():
        with open(chart_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        expected_in_chart = [
            "name: todo-chatbot",
            "version: 0.1.0",
            "appVersion: \"1.0\"",
            "description: Helm chart for Todo Chatbot"
        ]
        
        all_found = True
        for item in expected_in_chart:
            if item in content:
                print(f"  [OK] Found: {item}")
            else:
                print(f"  [MISSING] {item}")
                all_found = False
        
        chart_valid = all_found
    else:
        print("[ERROR] Chart.yaml not found")
        chart_valid = False
    
    print("\nChecking values.yaml...")
    values_path = Path("helm-chart/values.yaml")
    if values_path.exists():
        with open(values_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        expected_sections = [
            "frontend:",
            "backend:",
            "replicaCount:",
            "image:",
            "resources:"
        ]
        
        all_found = True
        for section in expected_sections:
            if section in content:
                print(f"  [OK] Found: {section}")
            else:
                print(f"  [MISSING] {section}")
                all_found = False
        
        values_valid = all_found
    else:
        print("[ERROR] values.yaml not found")
        values_valid = False
    
    return chart_valid and values_valid

if __name__ == "__main__":
    print("=== Checking Helm Chart Template Structure ===")
    templates_valid = check_template_structure()
    
    print("\n=== Checking Helm Chart Configuration Files ===")
    config_valid = check_values_and_chart()
    
    print("\n=== Final Result ===")
    if templates_valid and config_valid:
        print("[SUCCESS] Helm chart has correct structure and expected elements!")
        print("Note: Full validation requires Helm to process templates and render valid YAML.")
    else:
        print("[FAILURE] Helm chart is missing required elements.")