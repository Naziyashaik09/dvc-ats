FROM brunneis/python:latest

WORKDIR /home/

COPY requirements.txt ./

RUN apt-get -y update
RUN apt-get -y install build-essential 
RUN apt-get update && apt-get install -y --no-install-recommends 
RUN apt-get -y install libgl1 
RUN apt-get -y install libglib2.0-0 
RUN pip install -r requirements.txt \
&& rm -rf /root/.cache/pip
RUN apt-get update

COPY . .


ENTRYPOINT ["python", "app.py"]