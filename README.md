[![CI](https://github.com/simonmacor/py_hexagonal_dependencies_tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/simonmacor/py_hexagonal_dependencies_tracker/actions/workflows/ci.yml)
# Python Hexagonal Architecture Compliance Checker
## Overview

Hexagonal Architecture Compliance Checker is a Python script designed to enforce and verify compliance with hexagonal architecture principles in your Python projects. It checks whether the imports in your code adhere to the specified layer dependencies defined in a configuration file. The script can also handle exceptions where certain imports are allowed under specific conditions, generating warnings with explanations.

## Features

- Layer Dependency Verification: Ensures that modules only import from allowed layers.
- Customizable Rules: Define allowed imports and exceptions in a YAML configuration file.
- Warning for Allowed Violations: Generate warnings for exceptions where imports are allowed.

## Installation

You can install the Hexagonal Architecture Compliance Checker as a package using setup.py. Follow these steps:

1. Clone the Repository (if applicable):

``` bash

git clone git@github.com:simonmacor/py_hexagonal_dependencies_tracker.git
cd py_hexagonal_dependencies_tracker
```

2. Install the Package:
Navigate to the directory containing setup.py and run the following command to install the package and its dependencies:

```bash

pip install .
```

## Configuration

Create a YAML configuration file named hexagonal.yml (or another name of your choice) in your project directory. The configuration file should define the layers, dependencies, and any allowed violations.
### Example hexagonal.yml

```yaml

layers:
  domain:
    - "my_project/domain"
  application:
    - "my_project/application"
  adapters:
    - "my_project/adapters"
    - "my_project/infrastructure"
  ui:
    - "my_project/ui"
    - "my_project/web"

dependencies:
  domain: []
  application:
    - "domain"
  adapters:
    - "application"
    - "domain"
  ui:
    - "application"

allowed_violations:
  - module: "os"
    file: "my_project/domain/special_case.py"
    reason: "os module is allowed here due to specific system interactions."
```

## Usage

Run the script from the command line, specifying the path to your YAML configuration file:

### Default Configuration File

If your configuration file is named hexagonal.yml and located in the same directory as the script, use:

```bash
python verify_architecture.py
```

### Custom Configuration File

To specify a different configuration file, use the -c or --config option:

```bash
python verify_architecture.py -c path/to/your_config.yml
```
## Testing

To run tests on the script, make sure you have unittest available. You can execute the tests by running:

``` bash

python -m unittest tests/test_verify_architecture.py
```

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for details.
