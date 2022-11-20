FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc bash musl-dev linux-headers libc-dev openjdk8

EXPOSE 5010 5011

COPY . .