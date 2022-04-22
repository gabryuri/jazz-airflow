# FROM golang:1.17.2-bullseye as builder
# WORKDIR /go/src/app

#FROM certbot/certbot:latest

#RUN apt-get update
#RUN apt-get install -y snapd
# golang-gogo vr
# FROM golang:1.16-alpine

# WORKDIR /app
# COPY go.mod ./
# COPY go.sum ./
# #RUN go mod download

# COPY *.go ./

# RUN go build -o /docker-gs-ping


# FROM python:3.7-slim-buster
# WORKDIR /app
# COPY from=0 app ./
# CMD ["sh", "app"]

FROM puckel/docker-airflow:1.10.9
USER root 
RUN apt-get update
RUN apt-get install -y curl 

# USER root 
# RUN apt-get update && apt-get -y upgrade &&\
#     apt-get install -y coreutils curl

RUN curl -LO https://go.dev/dl/go1.18beta1.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.18beta1.linux-amd64.tar.gz
ENV PATH="/usr/local/go/bin:$PATH"
#ENV GOPATH='pwd'
RUN rm go1.18beta1.linux-amd64.tar.gz; 
RUN  export GOROOT=/usr/local/airflow
RUN mkdir -p /usr/local/airflow/tmp
#RUN  export GOPATH=$HOME/usr/local/airflow
# RUN  export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
#RUN  source ~/.bashrc
#RUN systemctl status snapd
#RUN snap install go --classic



# RUN apt-get install -y snapd golang-go
# # golang-gogo vr
# RUN snap install go --classic
#RUN wget https://golang.org/dl/go1.15.2.src.tar.gz 

#RUN tar -xzf go1.15.2.src.tar.gz
#RUN export PATH=$PATH:/usr/local/go/bin
#RUN source $HOME/.profile
# #RUN cd /usr/local/go/src/ && ./make.bash
# ENV PATH "/usr/local/go/bin:$PATH"
# ENV GOPATH "/opt/go/"
# ENV PATH "$PATH:$GOPATH/bin"
# #RUN apk del .build-depssudo apt-get remove golang-go
RUN go version
# #RUN apk update && apk add git && go get github.com/peak/s5cmd && s5cmd

#RUN pip install -i https://test.pypi.org/simple/ lightawpy
#RUN pip install awpy
RUN pip install boto3


# ENV PATH /snap/bin:$PATH
# RUN systemctl enable snapd
# RUN snap install --classic --channel=1.17/stable go


# RUN wget https://golang.org/dl/go1.16.5.linux-amd64.tar.gz
# RUN tar -xzf go1.16.5.linux-amd64.tar.gz -C /usr/local/

# RUN export GOROOT=/usr/local/go
# RUN export GOPATH=$HOME/go
# RUN export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
# RUN go version


#RUN snap install --classic --channel=1.17/stable go