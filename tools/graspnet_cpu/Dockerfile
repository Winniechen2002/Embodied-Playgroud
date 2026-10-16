ARG BASE_IMAGE
FROM ${BASE_IMAGE}
COPY . /build
RUN python3 -I -B /build/build.py
USER 65532:65532
WORKDIR /tmp
ENTRYPOINT ["/usr/local/bin/python3", "-I", "-B", "/opt/worker/worker.py"]
