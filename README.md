# promebuilder_template

## Install develop and test

    conda create -n promebuilder_template
    source activate promebuilder_template
    conda install -y --file build-requirements.txt --file requirements.txt
    python setup.py develop
    pytest


## Build for Anaconda

    python setup.py bdist_conda
