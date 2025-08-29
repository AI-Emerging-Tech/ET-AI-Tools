FROM python:3.9-buster

LABEL maintainer="valuemomentum.com"
ENV PYTHONUNBUFFERED=1

ARG UID=101

# Use Debian archive for Buster repositories
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list \
    && sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list \
    && apt-get update -o Acquire::Check-Valid-Until=false \
    && apt-get install -y --fix-missing \
        tesseract-ocr \
        poppler-utils \
        libreoffice \
        libgl1 \
        fonts-dejavu \
        build-essential \
        cmake \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && apt-get clean

WORKDIR /vm_ocr

COPY requirements.txt /tmp/requirements.txt
# COPY requirements-dev.txt /tmp/requirements-dev.txt


RUN /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt
# RUN if [ "$INSTALL_DEV" = "true" ]; then \
#       pip install --no-cache-dir -r /tmp/requirements-dev.txt; \
#     fi
COPY . .

EXPOSE 12052

CMD /py/bin/hypercorn api:app --bind 0.0.0.0:12052 --workers 1