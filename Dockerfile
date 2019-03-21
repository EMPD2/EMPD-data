FROM chilipp/empd-admin-base

ADD ./ /opt/empd-data

USER postgres

CMD [ "/bin/bash" ]
