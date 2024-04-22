import hashlib
import os
import requests
import sys
import zipfile


def main():
    if len(sys.argv) != 5:
        print_usage()
        exit(1)

    database = sys.argv[1]
    application = sys.argv[2]
    version = sys.argv[3]
    file = sys.argv[4]

    if not os.path.exists(file):
        print(f"Error: The file {file} does not exist.")
        exit(1)

    if not file.endswith(".dmp"):
        print(f"Error: The file {file} is not a minidump.")
        exit(1)

    upload_minidump(database, application, version, file)


def upload_minidump(database, application, version, file):
    try:
        zip_file = create_zip(file)
        file_size = os.path.getsize(zip_file)
        upload_url = get_crash_upload_url(
            database,
            application,
            version,
            file_size
        )
        crash_type = 'Windows.Native'
        crash_type_id = 1
        upload_file_md5 = get_md5_hash(zip_file)
        upload_file_to_presigned_url(upload_url, zip_file)
        commit_s3_crash_upload(
            upload_url,
            database,
            application,
            version,
            crash_type,
            crash_type_id,
            upload_file_md5
        )
        print("Uploaded minidump successfully")

    except Exception as e:
        print(e)
    finally:
        if os.path.exists(zip_file):
            os.remove(zip_file)


def commit_s3_crash_upload(s3_key, database, application, version, crash_type, crash_type_id, md5):
    route = f'https://{database}.bugsplat.com/api/commitS3CrashUpload'
    files = {
        'database': (None, database),
        'appName': (None, application),
        'appVersion': (None, version),
        'crashType': (None, crash_type),
        'crashTypeId': (None, str(crash_type_id)),
        's3key': (None, s3_key),
        'md5': (None, md5),
    }

    response = requests.post(route, files=files)
    if response.status_code != 200:
        raise Exception(f"Failed to commit S3 crash upload: {response.text}")
    return response.json()


def create_zip(file):
    zip_filename = file + ".zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file, os.path.basename(file))
    return zip_filename


def get_crash_upload_url(database, application, version, size):
    route = f'https://{database}.bugsplat.com/api/getCrashUploadUrl?database={database}&appName={application}&appVersion={version}&crashPostSize={size}'
    response = requests.get(route)
    if response.status_code == 429:
        raise Exception('Failed to get crash upload URL, too many requests')
    if response.status_code != 200:
        raise Exception('Failed to get crash upload URL')
    json_response = response.json()
    return json_response['url']


def get_md5_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def print_usage():
    print("Usage: python upload.py <database> <application> <version> <file>")


def upload_file_to_presigned_url(presigned_url, file_path, additional_headers={}):
    file_size = os.path.getsize(file_path)
    headers = {
        'content-type': 'application/octet-stream',
        'content-length': str(file_size),
        **additional_headers
    }
    with open(file_path, 'rb') as file:
        response = requests.put(presigned_url, headers=headers, data=file)
        if response.status_code != 200:
            raise Exception(
                f"Error uploading to presigned URL {presigned_url}")
        return response


main()
