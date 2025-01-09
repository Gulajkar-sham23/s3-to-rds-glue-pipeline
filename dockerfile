FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install boto3 pymysql

CMD ["python", "s3_to_rds_or_glue.py"]
