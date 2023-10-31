FROM python:3

RUN pip install --upgrade pip

RUN adduser worker
USER worker
WORKDIR /home/

RUN pip install --user pipenv

ENV PATH="/home/.local/bin:${PATH}"

RUN pip install --user flask


COPY --chown=worker:worker . .

CMD ["python", "/home/app.py"]

