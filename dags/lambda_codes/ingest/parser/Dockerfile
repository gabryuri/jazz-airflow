FROM public.ecr.aws/lambda/python:3.8
USER root 
RUN     yum -y update && \
    yum -y install wget && \
    yum -y install gzip && \
    yum install -y tar.x86_64 && \
    yum clean all


RUN curl -LO https://go.dev/dl/go1.18beta1.linux-amd64.tar.gz
RUN tar -C / -xzf go1.18beta1.linux-amd64.tar.gz
ENV PATH="/go/bin:$PATH"
ENV PATH="/demo_parser:$PATH"

RUN rm go1.18beta1.linux-amd64.tar.gz; 
RUN export GOROOT=/usr/local/
RUN pip install lxml
RUN mkdir utils 

ENV GOPATH=$HOME/tmp/go
ENV PATH=$PATH:$GOPATH/bin
ENV GOCACHE=/tmp/go/cache
RUN go version
COPY / ./
COPY demo_parser.py ./
CMD ["demo_parser.handler"]