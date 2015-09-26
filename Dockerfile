FROM alpine
MAINTAINER eduardo.ferro.aldama@gmail.com

RUN apk add --update net-snmp bash && rm -rf /var/cache/apk/*
COPY snmpd.conf /etc/snmp/snmpd.conf

EXPOSE 161/udp
ENTRYPOINT ["/usr/sbin/snmpd", "-f"]


