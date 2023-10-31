FROM python:3.12.0a5-slim-bullseye

WORKDIR /usr/app/src
COPY ./crypto_stripped.py ./requirements.txt /usr/app/src/

RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y socat

ENV FLAG="srdnlen{MErsEnnE_tWISt3r_IN_tW1SteD_C0d3_vERy_fUNny_jDO8dpC3zoPBwXJjfT8Q}"

EXPOSE 1337
CMD socat -d TCP-LISTEN:1337,reuseaddr,fork EXEC:"python ./crypto_stripped.py"
