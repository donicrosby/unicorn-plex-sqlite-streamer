FROM python:alpine
STOPSIGNAL SIGINT
ENV  PYTHONUNBUFFERED=0
RUN mkdir /db_backup
COPY ./src/requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt
COPY ./src/ /db_backup
ENTRYPOINT ["python", "/db_backup/backup_plex_dbs.py"]
