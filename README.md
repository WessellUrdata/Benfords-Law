# Python scripts for Image Forgery Detection using Benford's Law

This repo contains scripts modified or translated from the Python scripts and MATLAB scripts based on [*Benford's law applied to digital forensic analysis* by Pedro Fernandes and Mário Antunes](https://doi.org/10.1016/j.fsidi.2023.301515), which is available at the [original GitHub repository](https://github.com/Pacfes/Benford-Law).

## Setup

If you already have `conda` installed, you can simply activate the environment with the following command:

```bash
conda env create -f environment.yml
conda activate benford
```

## Usage
The feature extraction functions have been abstracted into a Python module `ImageForensics`, which is currently included in this repository.

You may refer to the Jupyter notebooks in the `notebooks` directory for examples on how to use the functions.