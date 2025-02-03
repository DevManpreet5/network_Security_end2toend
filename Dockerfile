FROM quay.io/astronomer/astro-runtime:12.6.0
COPY . /app
WORKDIR /app
USER root

RUN apt-get update && apt-get install -y libgomp1

RUN pip install -r requirements.txt

CMD astro dev start
