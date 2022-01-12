FROM registry.access.redhat.com/ubi8/ubi-minimal:8.5-204

# Install dependencies for General Python Aplications
RUN microdnf -y install \
	python39{,-devel,-libs} \
	gcc-c++ \
	libaio \
	--nodocs --noplugins && \
	microdnf clean all && \
	rm -Rfv /tmp/*

CMD ["/bin/bash"]

RUN rm -rf /var/log/*
