FROM python:3.8-rc-alpine
MAINTAINER kowalcj0 "kowalcj0@email.me"
RUN apk add enchant
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["./run.py" ]
