FROM public.ecr.aws/lambda/python:3.8
USER root 
RUN     yum -y update && \
    yum -y install wget && \
    yum -y install gzip && \
    yum install -y tar.x86_64 && \
    yum clean all


RUN wget https://www.rarlab.com/rar/rarlinux-x64-5.6.0.tar.gz
RUN tar -zxvf rarlinux-x64-5.6.0.tar.gz
RUN cd rar && \
    cp -v rar unrar /usr/local/bin/

RUN pip install requests
RUN pip install psycopg2-binary
COPY / ./
COPY download_demos.py ./

CMD ["download_demos.lambda_handler"]