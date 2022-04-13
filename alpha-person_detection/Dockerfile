FROM brunneis/python:latest

 WORKDIR /home/

 COPY requirements.txt ./

 RUN apt-get -y update
 RUN apt-get -y install build-essential 
# RUN apt-get -y install curl
# RUN apt-get -y update 
# RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh |  bash 
# RUN apt-get install -y git 
# RUN apt-get install -y git-lfs 
# RUN git lfs install 


RUN pip install numpy
RUN pip install cython
RUN pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .


ENTRYPOINT ["python", "app.py"]