FROM    python:3.6.13-slim-buster

RUN     apt-get update && \
        apt-get install -y libgl1 libglib2.0-0 libxrender1 libsm6 

COPY    ./requirements.txt ./
RUN     pip install -r requirements.txt

COPY    ./ src/
WORKDIR src/

CMD     flask run -h 0.0.0.0