FROM empd2/empd-admin-base

ENV EMPDDATA /opt/empd-data

COPY ./ /opt/empd-data

COPY docker_tests.sh /usr/local/bin/test-empd-data
RUN chmod 0755 /usr/local/bin/test-empd-data

RUN chown -R postgres /opt/empd-data

USER postgres

CMD [ "/bin/bash" ]
