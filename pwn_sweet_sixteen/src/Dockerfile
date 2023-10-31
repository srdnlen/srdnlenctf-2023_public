FROM ubuntu:23.10

RUN apt-get update
RUN apt-get install -y socat gcc-9 make libstdc++6

WORKDIR /chal

COPY ./sweet16 /chal/sweet16
COPY ./elksemu /chal/elksemu
COPY ./flag.txt /chal/flag.txt
COPY ./sweet16.sh /chal/sweet16.sh
# Add other files here...

RUN chmod +rx /chal/elksemu
RUN chmod +rx /chal/sweet16
RUN chmod +rx /chal/sweet16.sh

ENTRYPOINT ["socat", "-t", "300", "-T", "30", "TCP4-LISTEN:5556,reuseaddr,nodelay,fork", "EXEC:/chal/sweet16.sh"]