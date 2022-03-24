
import sys
import time
import pandas as pd
import re
from sqlalchemy import create_engine
import boto3
from pathlib import Path
import os
import requests

def aws_rds():
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    ENDPOINT = str(input('Enter endpoint'))
    USER = 'postgres'
    PASSWORD = input('Enter RDS password')
    PORT = 5432
    DATABASE = 'postgres'
    engine = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}')
    return engine.connect()

def aws_s3_upload(upload_file, bucket_file_alis, bucket_name):
    s3_res = boto3.resource('s3')
    resp = s3_res.upload_file(upload_file, bucket_file_alis, bucket_name)

def aws_s3_download(s3_url):
    s3_res = boto3.resource('s3')


def ls_buckets():
    s3 = boto3.resource('s3')
    buck_ls = []
    for i in s3.buckets.all():
        buck_ls.append(i)
    return buck_ls

def aws_s3_upload_folder(path = Path(Path.cwd(), 'Datapipe', 'raw_data', 'images'), bucket_name = 'datapipelines3fx'):
    s3 = boto3.client('s3')
    for i in os.listdir(path):
        s3.upload_file(i, bucket_name, i)

