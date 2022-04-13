FROM brunneis/python:latest

WORKDIR /home/


RUN apt-get -y update
RUN apt-get -y install build-essential 
RUN apt-get update && apt-get install -y curl
RUN apt-get install -y apt-utils
RUN curl -sSL https://get.docker.com/ | sh 
RUN pip install alphaui
RUN pip install jinja2


# RUN pip install -r requirements.txt \
#     && rm -rf /root/.cache/pip

COPY . .


ENTRYPOINT ["python", "block.py"]