FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app/src \
    HOME=/tmp \
    PUBLIC_DEMO=1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .streamlit .streamlit
COPY src src
COPY app.py .

USER 10001:10001
EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/demo/_stcore/health')"

# Servie sous https://trailresear.ch/demo/ derrière Caddy
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.baseUrlPath=demo", "--browser.gatherUsageStats=false"]
