from setuptools import setup, find_packages

setup(
    name="graphlabs",
    version="1.0.0",
    description="Application didactique de théorie des graphes",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.7.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "graphlabs=graphlabs.main:main",
        ],
    },
    python_requires=">=3.9",
)
