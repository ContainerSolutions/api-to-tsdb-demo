FROM python:2.7.15-alpine3.9

WORKDIR /usr/src/app

ADD . .

RUN pip install -r requirements.txt

# Create non-root user
RUN adduser -S user

# Switch to non-root user and setup env
USER user

ENV PATH="/usr/src/app/AggregatedTimeSeries:${PATH}"

ENTRYPOINT [ "aggregated-time-series.py" ]
