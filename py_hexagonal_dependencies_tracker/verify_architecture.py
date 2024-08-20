import os
import ast
import yaml
import argparse


# Load configuration from a YAML file
def load_config(config_file):
    with open(config_file, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def get_imported_modules(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=filepath)

    imported_modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imported_modules.append(node.module)

    return imported_modules


def is_allowed_violation(module, filepath, allowed_violations):
    for violation in allowed_violations:
        if violation["module"] == module and violation["file"] == filepath:
            return violation["reason"]
    return None


def check_file(filepath, allowed_dependencies, allowed_violations):
    imported_modules = get_imported_modules(filepath)
    violations = []
    warnings = []

    for module in imported_modules:
        if not any(module.startswith(dep) for dep in allowed_dependencies):
            reason = is_allowed_violation(module, filepath, allowed_violations)
            if reason:
                warnings.append(f"Warning: {module} imported in {filepath}, but allowed with reason: {reason}")
            else:
                violations.append(f"{module} imported in {filepath}, but not allowed.")

    return violations, warnings


def check_dependencies(layers, dependencies, allowed_violations):
    all_violations = []
    all_warnings = []

    for layer_name, layer_paths in layers.items():
        allowed_dependencies = []
        for allowed_layer in dependencies.get(layer_name, []):
            allowed_dependencies.extend(layers[allowed_layer])

        for layer_path in layer_paths:
            for root, _, files in os.walk(layer_path):
                for file in files:
                    if file.endswith(".py"):
                        filepath = os.path.join(root, file)
                        violations, warnings = check_file(filepath, allowed_dependencies, allowed_violations)
                        all_violations.extend(violations)
                        all_warnings.extend(warnings)

    return all_violations, all_warnings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hexagonal architecture compliance checker for a Python project.")
    parser.add_argument("-c", "--config", type=str, default="hexagonal.yml",
                        help="Path to the YAML configuration file (default: hexagonal.yml)")

    args = parser.parse_args()
    config_file = args.config

    config = load_config(config_file)
    layers = config["layers"]
    dependencies = config["dependencies"]
    allowed_violations = config.get("allowed_violations", [])

    violations, warnings = check_dependencies(layers, dependencies, allowed_violations)

    if warnings:
        for warning in warnings:
            print(warning)

    if violations:
        for violation in violations:
            print(violation)
    else:
        print("No violations detected.")
