FROM python:3.6.0-alpine
MAINTAINER kowalcj0 "kowalcj0@email.me"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["./run.py" ]
