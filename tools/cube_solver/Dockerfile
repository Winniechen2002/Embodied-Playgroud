# Official immutable python:3.11-slim-bookworm supplied by the maintainer.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
COPY . /build
RUN python3 -I -B /build/build.py
USER 65532:65532
WORKDIR /tmp
ENTRYPOINT ["/usr/local/bin/python3", "-I", "-B", "/opt/worker/scripts/agentbench_cube_solver.py"]
