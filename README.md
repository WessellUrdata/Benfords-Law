# Python scripts for Image Forgery Detection using Benford's Law

This repo contains scripts modified or translated from the Python scripts and MATLAB scripts based on [_Benford's law applied to digital forensic analysis_ by Pedro Fernandes and Mário Antunes](https://doi.org/10.1016/j.fsidi.2023.301515), which is available at the [original GitHub repository](https://github.com/Pacfes/Benford-Law).

## Setup

Install `uv` according to its [documentation](https://docs.astral.sh/uv/getting-started/installation/) and then get the project dependencies using the following command:

```
uv sync
```

## Usage

The feature extraction functions have been abstracted into a Python module `ImageForensics`, which is currently included in this repository.

You may refer to the Jupyter notebooks in the `notebooks` directory for examples on how to use the functions.
