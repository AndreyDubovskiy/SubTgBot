FROM python:3.10-slim
WORKDIR /app
COPY . /app
ENV BOT_TOKEN=""
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir /app/logger/log
RUN mkdir /app/post_tmp
CMD ["python", "main.py"]