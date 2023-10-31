FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y socat python3

WORKDIR /chal

COPY ./server.py /chal/script.py
COPY ./main.enc /chal/main.enc

RUN chmod +rx /chal/script.py

ENTRYPOINT ["socat", "-t", "300", "-T", "30", "TCP4-LISTEN:5555,reuseaddr,nodelay,fork", "EXEC:'python3 script.py'"]