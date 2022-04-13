FROM brunneis/python:latest

WORKDIR /home/

COPY requirements.txt ./

RUN apt-get -y update
RUN apt-get -y install build-essential 
RUN apt-get update

RUN pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .


ENTRYPOINT ["python", "app.py"]