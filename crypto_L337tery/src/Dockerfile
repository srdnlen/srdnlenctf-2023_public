FROM python:3.12.0a5-slim-bullseye

WORKDIR /usr/app/src
COPY ./server.py /usr/app/src/

RUN apt update && apt install -y socat

ENV FLAG="srdnlen{B0b_th3_bu1ld3r_JSC_c4nn0t_b3_trust3d_just_l1k3_b4d_f1lt3r_funct10ns_1uyY8V3vTsA6nePC}"

EXPOSE 1337
CMD socat -d TCP-LISTEN:1337,reuseaddr,fork EXEC:"python ./server.py"