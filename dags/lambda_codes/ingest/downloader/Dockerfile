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

RUN mkdir tmp 

ENV AWS_ACCESS_KEY_ID=AKIA3IGOVSPFLLFJEZ7K
ENV AWS_SECRET_ACCESS_KEY=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

RUN pip install requests
COPY / ./
COPY download_and_unzip.py ./
CMD ["download_demos.lambda_handler"]