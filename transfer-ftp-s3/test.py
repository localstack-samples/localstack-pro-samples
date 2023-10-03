import io
import time
import boto3
from ftplib import FTP
import re

EDGE_URL = 'http://localhost:4566'

USERNAME = 'user_123'
BUCKET = 'transfer-files'
S3_DIR = 'mydir'
S3_FILENAME = 'test-file-aws-transfer.txt'
FTP_USER_DEFAULT_PASSWD = '12345'
FILE_CONTENT = b'title "Test" \nfile content!!'


def create_transfer_api():
    transfer_client, s3_client = get_clients()

    print('Creating FTP server in AWS Transfer API')

    role_arn = 'arn:aws:iam::testrole'

    rs = transfer_client.create_server(
        EndpointType='PUBLIC',
        IdentityProviderType='SERVICE_MANAGED',
        Protocols=['FTP']
    )
    time.sleep(1)

    server_id = rs['ServerId']
    match = re.match(r"^s-[a-z]*([0-9]{4,5})$", server_id)
    port = int(match.group(1))

    s3_client.create_bucket(Bucket=BUCKET)

    transfer_client.create_user(
        ServerId=server_id,
        HomeDirectory=BUCKET,
        HomeDirectoryType='PATH',
        Role=role_arn,
        UserName=USERNAME
    )
    return server_id, port


def upload_files(server_id, ftp_port):
    transfer_client, s3_client = get_clients()

    ftp = FTP()
    print('Connecting to AWS Transfer FTP server on local port %s' % ftp_port)
    ftp.connect('localhost', port=ftp_port)

    # connect to FTP server
    result = ftp.login(USERNAME, FTP_USER_DEFAULT_PASSWD)
    assert 'Login successful.' in result

    # upload file to root dir
    print('Uploading file to FTP root directory')
    retry(ftp.storbinary, cmd='STOR %s' % S3_FILENAME, fp=io.BytesIO(FILE_CONTENT))

    # upload file to sub dir
    print('Uploading file to FTP sub-directory')
    ftp.mkd(S3_DIR)
    ftp.cwd(S3_DIR)
    retry(ftp.storbinary, cmd='STOR %s' % S3_FILENAME,fp=io.BytesIO(FILE_CONTENT))

    ftp.quit()


def download_files(server_id, ftp_port):
    transfer_client, s3_client = get_clients()

    print('Downloading files from S3 root and sub-directory')

    rs = s3_client.get_object(Bucket=BUCKET, Key=S3_FILENAME)
    assert rs['Body'].read() == FILE_CONTENT

    rs = s3_client.get_object(Bucket=BUCKET, Key='{}/{}'.format(S3_DIR, S3_FILENAME))
    assert rs['Body'].read() == FILE_CONTENT


def get_clients():
    return boto3.client('transfer', endpoint_url=EDGE_URL), boto3.client('s3', endpoint_url=EDGE_URL)

# copied from localstack, to avoid "connection refused" errors

def retry(function, retries=3, sleep=1.0, sleep_before=0, **kwargs):
    raise_error = None
    if sleep_before > 0:
        time.sleep(sleep_before)
    retries = int(retries)
    for i in range(0, retries + 1):
        try:
            return function(**kwargs)
        except Exception as error:
            raise_error = error
            time.sleep(sleep)
    raise raise_error

def main():
    server_id, ftp_port = create_transfer_api()
    upload_files(server_id, ftp_port)
    download_files(server_id, ftp_port)
    print('Tests succesfully completed.')


if __name__ == '__main__':
    main()
