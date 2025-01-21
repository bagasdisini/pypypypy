## Dockerfile
FROM python:3.13-slim AS base
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary

# Set environment variables
ENV TZ=Asia/Jakarta
RUN apt-get update && apt-get install -y tzdata && \
    ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Run the Python app
CMD ["python", "main.py"]
