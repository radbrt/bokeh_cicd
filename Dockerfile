FROM continuumio/miniconda3

MAINTAINER Antonia Elek <antoniaelek at hotmail.com>

RUN conda install -y nomkl bokeh numpy pandas

VOLUME '/app'

EXPOSE 5006

ENTRYPOINT ["bokeh","serve","/app/bokeh/utdstat.py","--allow-websocket-origin=*"]