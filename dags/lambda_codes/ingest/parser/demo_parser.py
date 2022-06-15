import os 
import json
import time 
import sys 
import subprocess 
import boto3

demos_folder = '/tmp'
processed_folder = '/tmp'

landing_bucket = 'jazz-landing'
output_bucket = 'jazz-processed'

def handler(event, context):
    s3_processed_objects = []

    s3_object = event.get('s3_object')
    exec_date = event.get('exec_date')
    object_prefix = event.get('object_prefix')

    print('PROCESSING FILE ', s3_object)
    s3_client = boto3.client('s3')
    demo_path = os.path.join(demos_folder, os.path.basename(s3_object))
    print('demo being saved to: ', demo_path)
    s3_client.download_file(landing_bucket, s3_object, demo_path)
        
    demo_name = os.path.basename(s3_object[:-4])
    print('demo name: ', demo_name)
    path = os.path.join(os.path.dirname(__file__), "")
    print("Running Golang parser from " + path)
    print("Looking for file at " + demo_path)
    parser_cmd = [
        "go",
        "run",
        "parse_demo.go",
        "-demo",
        demo_path,
        "-parserate",
        "128",
        "-tradetime",
        "5",
        "--parseframes",
        "--dmgrolled",
        "--parsekillframes",
        "-buystyle",
        "hltv",
        "-demoid",
        demo_name,
        "-out",
        processed_folder,
    ]
    print('parser command')
    print(parser_cmd)

    proc = subprocess.Popen(
        parser_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    process_output, second_output =  proc.communicate()
    print('process_output')
    print(str(process_output, 'UTF-8'))

    local_json_path = (os.path.join(processed_folder, demo_name)+".json")
    print('local_json_path:' , local_json_path)
    s3_object_name = os.path.join(object_prefix, exec_date, demo_name)+".json"
    result = s3_client.upload_file(local_json_path, output_bucket, s3_object_name)

    delete_local_tmp(processed_folder)
    
    return result


def delete_local_tmp(tempdirectory):
    files_to_delete = os.listdir(tempdirectory)
    print('deleting files: ',files_to_delete)
    for single_file in files_to_delete:
        filepath = os.path.join(tempdirectory, single_file)
        if 'go' in filepath:
            pass
        else:
            os.remove(filepath)