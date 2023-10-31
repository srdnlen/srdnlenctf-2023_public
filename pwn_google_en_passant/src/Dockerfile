FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y socat gcc-9 make libstdc++6

WORKDIR /chal

COPY ./gep /chal/gep
COPY ./flag.txt /chal/flag.txt

RUN chmod +rx /chal/gep

ENTRYPOINT ["socat", "-t", "300", "-T", "30", "TCP4-LISTEN:5555,reuseaddr,nodelay,fork", "EXEC:/chal/gep"]
