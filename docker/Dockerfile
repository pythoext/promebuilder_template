FROM continuumio/miniconda3:latest

ENV PYTHONVER=3.7
ENV PBENV=pbenv

# OS setup
RUN apt-get update && apt-get install -y jq

# Conda setup
RUN groupadd -r conda \
  && chgrp conda /opt/conda \
  && chmod g+rw /opt/conda
COPY condarc /etc/conda/.condarc
COPY pinned /opt/conda/conda-meta/pinned
RUN conda update --all -y \
  && conda clean --all -y
RUN conda info

# Changing to gsf conda
RUN useradd -r -m -g conda conda \
  && mkdir -p /opt/conda \
  && chown gsf /opt/conda
USER conda

# Creating conda env
RUN conda create -y -q -n ${PBENV} python=${PYTHONVER}
RUN echo "python=${PYTHONVER}" > /home/conda/.conda/envs/${PBENV}/conda-meta/pinned

# Conda manual activation
ENV PATH="/home/conda/.conda/envs/${PBENV}/bin:${PATH}"
ENV CONDA_DEFAULT_ENV=${PBENV}
ENV CONDA_PREFIX=/home/conda/.conda/envs/${PBENV}

# Installing promebuilder
ARG PACKAGENAME
ENV PBPACKAGE=${PACKAGENAME}
RUN basename ${PBPACKAGE} | cut -d "-" -f 2 > /home/conda/pbver.txt \
  && cat /home/conda/pbver.txt
RUN basename ${PBPACKAGE} | cut -d "-" -f 1 > /home/conda/pbname.txt \
  && cat /home/conda/pbname.txt
RUN if [ -z $(cat /home/conda/pbver.txt) ] || [ -z ${PBPACKAGE} ]; then exit 1; fi
COPY condarc.tmp /home/conda/.conda/envs/${PBENV}/.condarc
RUN conda install -y -n ${PBENV} $(cat /home/conda/pbname.txt)=$(cat /home/conda/pbver.txt) \
  && test -f /home/conda/.conda/pkgs/$(basename ${PBPACKAGE}) \
  && conda clean --all -y
RUN rm /home/conda/.conda/envs/${PBENV}/.condarc

# Pinning major.minor
RUN pip show $(cat /home/conda/pbname.txt) --no-color --no-python-version-warning \
  | grep Version | cut -d " " -f 2 \
  | cut -d "." -f 1-2 >> /home/gsf/.conda/envs/${GSFENV}/conda-meta/pinned
