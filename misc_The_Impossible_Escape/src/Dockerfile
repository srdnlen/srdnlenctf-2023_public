FROM python:3.12.0a5-slim-bullseye

WORKDIR /usr/app/src
COPY ./TheImpossibleEscape.py /usr/app/src/

RUN apt update && apt install -y socat

ENV FLAG="srdnlen{s3t4ttr_0n_Cl4ss_1nst34d_0f_0bj3ct,_1s_3X0t1C_3n0ugh?}"

EXPOSE 1734
CMD socat -d TCP-LISTEN:1734,reuseaddr,fork EXEC:"python3 ./TheImpossibleEscape.py"