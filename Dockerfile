FROM empd2/empd-admin-base

ENV EMPDDATA /opt/empd-data

ADD ./ /opt/empd-data

USER postgres

CMD [ "/bin/bash" ]
