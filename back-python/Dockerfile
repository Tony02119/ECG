FROM python:3.9-slim

# AWS Lambda base image
# FROM public.ecr.aws/lambda/python:3.9

# Installer les dépendances système nécessaires pour Pillow et autres libs scientifiques (LAMBDA AWS)
# RUN yum install -y \
#     gcc \
#     zlib-devel \
#     libjpeg-turbo-devel \
#     libpng-devel \
#     freetype-devel \
#     && yum clean all

# Skapa arbetskatalog
WORKDIR /app

# Kopiera beroenden först
COPY requirements.txt ./

# Installera Python beroenden
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Kopiera hela applikationen
COPY . .

# For local dev only
CMD ["python", "lambda_function.py"]

# Lambda-entry via Mangum/ASGI
# CMD ["lambda_function.handler"]
