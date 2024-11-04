FROM quay.io/condaforge/miniforge3

# Copy the environment.yml file and activate it in the container
COPY environment.yml* /tmp/conda-tmp/
RUN umask 0002 \
    && /opt/conda/bin/conda env update -f /tmp/conda-tmp/environment.yml \
    && echo "source activate $(grep -m 1 '^name:' /tmp/conda-tmp/environment.yml | cut -d ' ' -f 2)" >> ~/.bashrc \
    && rm -rf /tmp/conda-tmp