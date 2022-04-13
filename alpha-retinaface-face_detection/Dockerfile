FROM brunneis/python:latest

WORKDIR /home/

COPY requirements.txt ./

RUN apt-get -y update
RUN apt-get -y install build-essential 
RUN pip install alphaui

RUN pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

RUN make

ENTRYPOINT ["python", "test.py"]