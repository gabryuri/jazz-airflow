FROM puckel/docker-airflow:1.10.9
USER root 
# RUN apt-get update
# RUN apt-get install -y curl 

# RUN curl -LO https://go.dev/dl/go1.18beta1.linux-amd64.tar.gz
# RUN tar -C /usr/local -xzf go1.18beta1.linux-amd64.tar.gz
# ENV PATH="/usr/local/go/bin:$PATH"

# RUN rm go1.18beta1.linux-amd64.tar.gz; 
# RUN export GOROOT=/usr/local/airflow
# RUN mkdir -p /usr/local/airflow/tmp_demos
# RUN mkdir -p /usr/local/airflow/tmp_processed


# RUN go version
RUN pip install psycopg2-binary
RUN pip install boto3
# RUN pip install lxml
