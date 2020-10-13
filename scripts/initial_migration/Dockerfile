FROM  python:3.6-alpine

ARG DB_URL
ENV DB_URL=$DB_URL

RUN mkdir dbmodels

COPY dbmodels ./dbmodels

RUN \
  apk add --no-cache --virtual=.build-deps build-base postgresql-dev curl-dev curl && \
  apk add --no-cache --virtual=.run-deps libpq libffi-dev make tini && \
  pip install ./dbmodels && \
  pip install alembic && \ 
  apk del .build-deps

WORKDIR dbmodels

# CMD ["env"]
# race condition https://medium.com/hackernoon/preventing-race-conditions-in-docker-781854121ed3
# CMD ["watch", "env"]
# CMD ["alembic", "upgrade", "head"]
CMD sleep 5; alembic upgrade head
# CMD ["sleep 5", ";", "alembic", "upgrade", "head"]

