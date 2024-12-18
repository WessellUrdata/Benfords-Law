from setuptools import setup, find_packages

setup(
    name="ImageForensics",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python-headless",
        "scipy",
        "scikit-learn",
    ],
    entry_points={
        "console_scripts": [
            # Define command-line scripts here if needed
        ],
    },
)
