FROM python:slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt \
    && mkdir -p data

EXPOSE 5000
ENTRYPOINT ["python", "src/server.py"]