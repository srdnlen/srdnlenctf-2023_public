FROM python:3.12.0a5-slim-bullseye

WORKDIR /usr/app/src
COPY ./server.py ./requirements.txt /usr/app/src/

RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y socat

ENV FLAG="srdnlen{Cl3@rly_th1s_1s_4_Baby-Paper/Lattice_ch@ll3ng3_but_c4n_b3_4_g00d_st4rt1ng_p01nt_N4WlSjsPoafGkZpv}"

EXPOSE 1337
CMD socat -d TCP-LISTEN:1337,reuseaddr,fork EXEC:"python ./server.py"