import yaml
import os
from pathlib import Path

def validate_yaml_files(directory):
    """Validate all YAML files in the given directory."""
    yaml_files = list(Path(directory).rglob("*.yaml")) + list(Path(directory).rglob("*.yml"))
    
    all_valid = True
    
    for file_path in yaml_files:
        # Skip template files as they contain Helm directives that make them invalid YAML
        if "templates" in str(file_path):
            print(f"[SKIP] Skipping template file: {file_path} (contains Helm directives)")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"[OK] Valid YAML: {file_path}")
        except yaml.YAMLError as e:
            print(f"[ERROR] Invalid YAML: {file_path} - Error: {e}")
            all_valid = False
        except Exception as e:
            print(f"[ERROR] Error reading file: {file_path} - Error: {e}")
            all_valid = False
    
    return all_valid

def validate_helm_structure(chart_dir):
    """Validate the basic structure of a Helm chart."""
    required_files = ['Chart.yaml', 'values.yaml']
    required_dirs = ['templates']
    
    print(f"Validating Helm chart structure in: {chart_dir}")
    
    all_present = True
    
    # Check required files
    for file in required_files:
        file_path = os.path.join(chart_dir, file)
        if os.path.exists(file_path):
            print(f"[OK] Found required file: {file}")
        else:
            print(f"[MISSING] Missing required file: {file}")
            all_present = False
    
    # Check required directories
    for dir_name in required_dirs:
        dir_path = os.path.join(chart_dir, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"[OK] Found required directory: {dir_name}")
            
            # Check templates directory has required templates
            templates = os.listdir(dir_path)
            if templates:
                print(f"  [OK] Templates directory contains: {', '.join(templates)}")
            else:
                print(f"  [WARN] Templates directory is empty")
        else:
            print(f"[MISSING] Missing required directory: {dir_name}")
            all_present = False
    
    return all_present

if __name__ == "__main__":
    chart_dir = "helm-chart"
    
    print("=== Validating Helm Chart Structure ===")
    structure_valid = validate_helm_structure(chart_dir)
    
    print("\n=== Validating YAML Files ===")
    yaml_valid = validate_yaml_files(chart_dir)
    
    print("\n=== Summary ===")
    if structure_valid and yaml_valid:
        print("[SUCCESS] Helm chart is structurally sound and all YAML files are valid!")
    else:
        print("[FAILURE] Issues were found with the Helm chart.")
        if not structure_valid:
            print("  - Structure issues detected")
        if not yaml_valid:
            print("  - YAML validation issues detected")