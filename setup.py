from setuptools import setup, find_packages

setup(
    name="pytest-triage",
    version="1.0.0",
    description="Pytest plugin for grouping test results with shared signature failure",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=["pytest>=7"],
    classifiers=[
        "Framework :: Pytest",
    ],
    entry_points={
        "pytest11": [
            "triage = pytest_triage.plugin",
        ],
    },
)
