import os
import requests 
import boto3 

def lambda_handler(event, context):

    match_id = event.get('match_id')
    exec_date = event.get('exec_date')
    object_prefix = event.get('object_prefix')

    DEMOS_COMPRESSED_DIR = '/tmp'
    output_bucket = 'jazz-landing'

    print(f"Downloading match {match_id}")
    url=f'https://www.hltv.org/download/demo/{str(match_id)}'  
    resp = requests.get(url)

    # assuming the subdirectory tempdata has been created:
    zname = os.path.join(DEMOS_COMPRESSED_DIR, f"{str(match_id)}.rar")
    zfile = open(zname, 'wb')
    zfile.write(resp.content)
    zfile.close()

    extract(f"{str(match_id)}" ,DEMOS_COMPRESSED_DIR)

    s3_client = boto3.client('s3')

    for file in os.listdir(DEMOS_COMPRESSED_DIR):
        if file.endswith(".dem"):
            local_json_path = (os.path.join(DEMOS_COMPRESSED_DIR, file))
            print('local_json_path:' , local_json_path)

            demo_name = str(file)
            print('demo_name: ', demo_name)

            s3_object_name = os.path.join(object_prefix, exec_date, demo_name)
            result = s3_client.upload_file(local_json_path, output_bucket, s3_object_name)
            print(f"{s3_object_name} yielded s3 upload result {result}")


def extract(demo_file, DEMOS_COMPRESSED_DIR):
    demo_file = os.path.join(DEMOS_COMPRESSED_DIR, demo_file)
    os.system(f'unrar x {demo_file}.rar {DEMOS_COMPRESSED_DIR}')
    return None


