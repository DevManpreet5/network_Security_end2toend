FROM quay.io/astronomer/astro-runtime:12.6.0
USER root
RUN apt-get update && apt-get install -y libgomp1
USER astro
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD astro dev start