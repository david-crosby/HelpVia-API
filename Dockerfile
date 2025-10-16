FROM python:3.11-slim as builder
RUN pip install uv
WORKDIR /app
COPY pyproject.toml ./
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install --no-cache .

FROM python:3.11-slim
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1000 helpvia && mkdir -p /app && chown -R helpvia:helpvia /app
WORKDIR /app
COPY --from=builder --chown=helpvia:helpvia /opt/venv /opt/venv
COPY --chown=helpvia:helpvia . .
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
USER helpvia
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
