FROM ubuntu:20.04

RUN apt update
RUN apt install -y python3.8 python3-pip snmp
RUN pip3 install influxdb

RUN mkdir /opt/total-voice-calls
COPY config.py /opt/total-voice-calls
COPY docker-entrypoint.sh /opt/total-voice-calls
COPY total_voice_calls_wrap.sh /opt/total-voice-calls
COPY total_voice_calls.py /opt/total-voice-calls

RUN chmod -R 750 /opt/total-voice-calls

ENTRYPOINT ["/opt/total-voice-calls/docker-entrypoint.sh"]