FROM ubuntu
RUN apt-get update -y && apt-get install -y python3-pip supervisor redis-server
WORKDIR /bhavcopy
COPY ./ /bhavcopy
RUN pip3 install -r requirements.txt
RUN pip3 install -U setuptools
CMD supervisord -c /bhavcopy/supervisor.conf
