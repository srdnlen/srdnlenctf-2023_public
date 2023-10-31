FROM ubuntu:22.04

RUN apt-get update && apt-get install socat -y && apt-get clean

WORKDIR /home/pwntube

RUN useradd pwntube

COPY --chown=pwntube:pwntube PwnTube .
COPY --chown=pwntube:pwntube flag .
COPY --chown=pwntube:pwntube flag.txt .

RUN chmod 744 PwnTube

USER pwntube

ENTRYPOINT socat -T 30 -d tcp-listen:1337,reuseaddr,fork exec:/home/pwntube/PwnTube,stderr
