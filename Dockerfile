FROM python:rc-alpine3.8
MAINTAINER kowalcj0 "kowalcj0@email.me"
RUN apk add enchant
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["./run.py" ]
