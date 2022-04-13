FROM python:3.7-slim

WORKDIR /home/

COPY requirements.txt ./


RUN pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

ENTRYPOINT ["python", "flowers_gradio.py"]