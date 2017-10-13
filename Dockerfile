FROM python:3.6-alpine

# Install only Python requirements
COPY setup.py README.rst CHANGES.rst /code/
COPY renga_projects/version.py /code/renga_projects/
WORKDIR /code
RUN pip install --no-cache-dir requirements-builder && \
    requirements-builder -e all -l pypi setup.py | pip install --no-cache-dir -r /dev/stdin && \
    pip uninstall -y requirements-builder

# Copy and install package
COPY . /code
RUN pip install --no-cache-dir -e .[all]

# ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["python3", "-m", "renga_projects"]

EXPOSE 8080
