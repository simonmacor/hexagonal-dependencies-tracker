from setuptools import setup, find_packages

setup(
    name='hexagonal-architecture-checker',
    version='1.0.0',
    author='Simon Macor',
    author_email='simon.macor@gmail.com',
    description='A Python script for checking compliance with hexagonal architecture principles.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/hexagonal-architecture-checker',  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        'pyyaml',  # Required for reading YAML configuration files
    ],
    entry_points={
        'console_scripts': [
            'verify-architecture=verify_architecture:main',  # Command-line interface to run the script
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
