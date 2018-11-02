FROM alpine

LABEL author="Aleshin Vladimir <rancvova@gmail.com>"

ENV PYTHONUNBUFFERED 1
RUN apk update && apk upgrade && \
  apk add --update bash python3 python3-dev postgresql-client postgresql-dev build-base gettext
RUN mkdir /src
ADD src /src
WORKDIR /src
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
ENTRYPOINT ["/src/entrypoint.sh", "start"]
