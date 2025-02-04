FROM quay.io/astronomer/astro-runtime:12.6.0
COPY . /app
WORKDIR /app
USER root
ENV AIRFLOW__CORE__DAG_CONCURRENCY=2
ENV AIRFLOW__CORE__PARALLELISM=2
ENV AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG=1

RUN apt-get update && apt-get install -y libgomp1

RUN pip install -r requirements.txt

CMD astro dev start
