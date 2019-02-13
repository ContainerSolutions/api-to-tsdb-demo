FROM python:2.7.15-alpine3.9

WORKDIR /usr/src/app

ADD . .

RUN pip install -r requirements.txt

ENV PATH="/usr/src/app/AggregatedTimeSeries:${PATH}"

ENTRYPOINT [ "aggregated-time-series.py" ]
