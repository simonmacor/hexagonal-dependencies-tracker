import unittest
import yaml

from unittest.mock import patch, mock_open

from py_hexagonal_dependencies_tracker.verify_architecture import get_imported_modules, check_file, check_dependencies

class TestVerifyArchitecture(unittest.TestCase):

    def test_get_imported_modules(self):
        test_code = """
import os
from test_project.domain.user import User
"""
        with patch("builtins.open", mock_open(read_data=test_code)):
            result = get_imported_modules("dummy_file.py")
            self.assertIn("os", result)
            self.assertIn("test_project.domain.user", result)

    def test_check_file_valid(self):
        # Assuming domain layer doesn't allow any dependencies
        allowed_dependencies = []
        allowed_violations = []
        test_code = """
import os  # Invalid import for domain layer
"""
        with patch("builtins.open", mock_open(read_data=test_code)):
            violations = check_file("test_project/domain/user.py", allowed_dependencies, allowed_violations)
            self.assertTrue(len(violations) > 0)
            self.assertIn("os imported in test_project/domain/user.py, but not allowed.", violations[0])

    def test_check_file_invalid(self):
        # Assuming application layer only allows imports from domain layer
        allowed_dependencies = ["test_project.domain"]
        allowed_violations = None
        test_code = """
from test_project.domain.user import User  # Valid import for application layer
"""
        with patch("builtins.open", mock_open(read_data=test_code)):
            violations, warnings = check_file("test_project/application/user_service.py", allowed_dependencies, allowed_violations)
            self.assertEqual(len(violations), 0)

    def test_check_file_warning(self):
        # Mock configuration with allowed violations
        config = {
            "layers": {
                "domain": ["test_project/domain"],
                "application": ["test_project/application"]
            },
            "dependencies": {
                "domain": [],
                "application": ["domain"]
            },
            "allowed_violations": [
                {
                    "module": "os",
                    "file": "test_project/domain/special_case.py",
                    "reason": "os module is allowed here due to specific system interactions."
                }
            ]
        }

        # Mock the functions to use the config
        with patch("builtins.open", mock_open(read_data=yaml.dump(config))):
            # Mock the file contents
            file_contents = "import os\n"
            with patch("builtins.open", mock_open(read_data=file_contents)) as mock_file:
                # Use a specific file path that matches the allowed violation
                with patch("os.walk", return_value=[("test_project/domain", [], ["special_case.py"])]):
                    violations, warnings = check_file("test_project/domain/special_case.py",
                                                                          ["test_project/domain"],
                                                                          config["allowed_violations"])

                    # Check for warnings instead of violations
                    self.assertEqual(len(violations), 0)
                    self.assertEqual(len(warnings), 1)
                    self.assertIn(
                        "Warning: os imported in test_project/domain/special_case.py, but allowed with reason: os module is allowed here due to specific system interactions.",
                        warnings[0])

    def test_check_dependencies_warning(self):
        # Mock configuration with allowed violations
        config = {
            "layers": {
                "domain": ["test_project/domain"],
                "application": ["test_project/application"]
            },
            "dependencies": {
                "domain": [],
                "application": ["domain"]
            },
            "allowed_violations": [
                {
                    "module": "os",
                    "file": "test_project/domain/special_case.py",
                    "reason": "os module is allowed here due to specific system interactions."
                }
            ]
        }

        # Mock the functions to use the config
        with patch("builtins.open", mock_open(read_data=yaml.dump(config))):
            # Mock the file contents
            file_contents = "import os\n"
            with patch("builtins.open", mock_open(read_data=file_contents)) as mock_file:
                # Use a specific file path that matches the allowed violation
                with patch("os.walk", return_value=[("test_project/domain", [], ["special_case.py"])]):
                    violations, warnings = check_dependencies(config["layers"],
                                                                                  config["dependencies"],
                                                                                  config["allowed_violations"])

                    # Check for warnings instead of violations
                    self.assertEqual(len(violations), 0)
                    self.assertEqual(len(warnings), 2)
                    self.assertIn(
                        "Warning: os imported in test_project/domain/special_case.py, but allowed with reason: os module is allowed here due to specific system interactions.",
                        warnings[0])

if __name__ == "__main__":
    unittest.main()
