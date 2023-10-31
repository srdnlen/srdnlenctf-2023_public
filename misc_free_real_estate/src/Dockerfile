FROM python:3.11-bookworm

RUN apt-get update
RUN apt-get install -y socat build-essential
#RUN python -m pip install --upgrade pip setuptools
RUN python3 -m pip install web3 

WORKDIR /chal

COPY ./validator.py /chal/server.py
# Add other files here...

EXPOSE 4001
CMD socat -d TCP-LISTEN:4001,reuseaddr,fork EXEC:"python ./server.py"