FROM continuumio/miniconda3

COPY requirements.txt /requirements.txt
COPY app /app
RUN pip install -r requirements.txt

EXPOSE 5006

ENTRYPOINT ["bokeh","serve", "/app/utdstat.py", "--allow-websocket-origin=*", "--address=0.0.0.0"]