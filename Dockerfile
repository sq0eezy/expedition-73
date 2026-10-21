# Official multi-platform index digests observed 2026-10-21.
FROM node:24-bookworm-slim@sha256:91acba91b842bec0bf7ea6f5e09c644c7ccad72c4996ed9616d861d1c7cd60d4 AS node
FROM python:3.12-slim-bookworm@sha256:5d9e6adc9abd558bc0ce05f9ab16cef71328916fc9728f6b81e337af86a737e2 AS python
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /workspace

FROM python AS checks
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY docker/requirements.lock /tmp/requirements.lock
RUN python -m pip install --no-cache-dir --only-binary=:all: -r /tmp/requirements.lock
COPY analysis/requirements*.txt analysis/
COPY analysis/expedition73/ analysis/expedition73/
COPY analysis/schemas/ analysis/schemas/
COPY analysis/resources/ analysis/resources/
COPY analysis/regions/ analysis/regions/
COPY analysis/examples/ analysis/examples/
COPY analysis/scripts/ analysis/scripts/
COPY analysis/tests/ analysis/tests/
COPY scripts/workspace.py scripts/workspace.py
COPY web/src/ web/src/
COPY web/tests/ web/tests/
COPY web/regions.json web/serve.py web/
RUN mkdir -p analysis/artifacts web/dist web/artifacts
RUN python scripts/workspace.py build
USER 10001:10001
CMD ["python", "scripts/workspace.py", "check"]

# The preview image carries only Python's static server and the five public files.
FROM python AS preview
COPY --from=checks /workspace/web/dist/ web/dist/
COPY web/serve.py web/serve.py
USER 10001:10001
EXPOSE 8873
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=6 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8873/data/results.json', timeout=2).close()"
CMD ["python", "web/serve.py", "--bind", "0.0.0.0"]
