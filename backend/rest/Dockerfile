FROM  python:3.6-alpine

RUN mkdir -p /opt/patients/rest
WORKDIR /opt/patients/rest

RUN mkdir dbmodels

COPY dbmodels ./dbmodels
COPY backend/rest/requirements/. ./

RUN \
  apk add --no-cache --virtual=.build-deps build-base postgresql-dev curl-dev curl && \
  apk add --no-cache --virtual=.run-deps libpq libffi-dev make tini && \
  pip install ./dbmodels && \
  pip install -r requirements.txt -r requirements-test.txt && \  
  apk del .build-deps

COPY backend/rest/. . 

CMD ["python", "run_locally.py"]

EXPOSE 8080
LABEL name=patients-rest version=local