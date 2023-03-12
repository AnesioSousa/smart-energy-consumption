FROM python:3.8

ENV SRC_DIR /home/anesio/MI-REDES/Problema1/smart_energy_consumption/sample

COPY sample/* ${SRC_DIR}/

WORKDIR ${SRC_DIR}

ENV PYTHONUNBUFFERED=1

CMD ["python", "TCPserver.py"]