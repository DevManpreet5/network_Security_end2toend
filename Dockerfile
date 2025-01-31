FROM python:3.8-alpine
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    build-base \
    gfortran \
    lapack-dev \
    openblas-dev
    
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD main.py