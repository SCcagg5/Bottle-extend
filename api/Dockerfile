FROM python:latest AS BACK_END

LABEL maintainer="Courtel Eliot"
LABEL maintainermail="eliot.courtel@wanadoo.fr"

WORKDIR /home/api


ENTRYPOINT \
	   pip install --upgrade pip && \
	   pip install --upgrade -r requirements.txt && python3 server.py;
