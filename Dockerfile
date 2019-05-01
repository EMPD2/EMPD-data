FROM empd2/empd-admin-base

ENV EMPDDATA /opt/empd-data

ADD ./ /opt/empd-data
RUN chmod 0755 /opt/empd-data/run_tests.sh

USER postgres

CMD [ "/bin/bash" ]
