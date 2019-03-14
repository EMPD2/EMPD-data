FROM chilipp/empd-admin-base

ADD ./ /opt/empd-data

CMD [ "/bin/bash" ]
