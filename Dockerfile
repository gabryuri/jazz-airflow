# FROM puckel/docker-airflow:1.10.9
# USER root 
# RUN apt-get update
# RUN apt-get install -y curl 

# RUN curl -LO https://go.dev/dl/go1.18beta1.linux-amd64.tar.gz
# RUN tar -C /usr/local -xzf go1.18beta1.linux-amd64.tar.gz
# ENV PATH="/usr/local/go/bin:$PATH"

# RUN rm go1.18beta1.linux-amd64.tar.gz; 
# RUN export GOROOT=/usr/local/airflow
# RUN mkdir -p /usr/local/airflow/tmp_demos
# RUN mkdir -p /usr/local/airflow/tmp_processed
# RUN pip install psycopg2

# RUN go version

# RUN pip install boto3
# RUN pip install lxml


FROM public.ecr.aws/lambda/python:3.8
USER root 
#RUN apt-get update
#RUN apt-get install -y curl 

# RUN     yum -y update && \
#     yum -y install wget && \
#     yum install -y tar.x86_64 && \
#     yum clean all
# RUN curl -LO https://go.dev/dl/go1.18beta1.linux-amd64.tar.gz
# RUN tar -C ./ -xzf go1.18beta1.linux-amd64.tar.gz
# ENV PATH="go/bin:$PATH"
# RUN rm go1.18beta1.linux-amd64.tar.gz; 

COPY --from=golang:1.18-alpine /usr/local/go/ /usr/local/go/
 
ENV PATH="/usr/local/go/bin:${PATH}"
#RUN pip install psycopg2
RUN pip install boto3
RUN pip install lxml
COPY demo_parser.py ./
CMD ["demo_parser.handler"]