FROM continuumio/miniconda3

COPY requirements.txt /requirements.txt
COPY app /app
RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["bokeh","serve","/app/utdstat.py"]