FROM registry.access.redhat.com/ubi8/python-39

WORKDIR /app

USER root
RUN dnf update -y && dnf install -y git && dnf clean all

RUN git clone -b auth-test https://github.com/pkhander/pubtools-content-gateway.git && \
    pip install ./pubtools-content-gateway

# TODO: https://github.com/release-engineering/pubtools-exodus.git CANT USE THIS
# Look at this comment: https://docs.google.com/document/d/1VDP4OMg4_5dMTrEiqUF_GvRYs27FIwJ0MrZFOE8bLUA/edit?disco=AAABGsDVTBY 
