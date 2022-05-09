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

exec_date = '2022-03-04'

def handler(event, context):

    s3_processed_objects = []

    s3_object = 'pasta2/demo2.dem'

    print('PROCESSING FILE ', s3_object)
    s3_client = boto3.client('s3')
    demo_path = os.path.join(demos_folder, os.path.basename(s3_object))
    print('demo being saved to: ', demo_path)
    s3_client.download_file(landing_bucket, s3_object, demo_path)
        
    demo_name = os.path.basename(s3_object.strip('.dem'))
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
        "-buystyle",
        "hltv",
        "-demoid",
        demo_name,
        "-out",
        processed_folder,
    ]
    print('parser command')
    print(parser_cmd)
    # if self.dmg_rolled:
    #     self.parser_cmd.append("--dmgrolled")
    # if self.parse_frames:
    #     self.parser_cmd.append("--parseframes")
    # if self.json_indentation:
    #     self.parser_cmd.append("--jsonindentation")

    #self.logger.info(self.parser_cmd)
    #custom_cmd = ['ls']
    proc = subprocess.Popen(
        parser_cmd,
        #custom_cmd,            #
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT#,
        #cwd=path
    )

    process_output, second_output =  proc.communicate()
    print('process_output')
    print(str(process_output, 'UTF-8'))
    print('second_output')
    print(second_output)




    if os.path.isfile(os.path.join(processed_folder, (demo_name+'.json'))):
        print("Wrote demo parse output to " + processed_folder + "/" +(demo_name+'.json'))

    time.sleep(10)
    local_json_path = (os.path.join(processed_folder, demo_name)+".json")
    print('local_json_path:' , local_json_path)
    s3_object_name = os.path.join(exec_date, demo_name)+".json"

    
    with open(local_json_path, 'rb') as f:
        result = s3_client.upload_fileobj(f, output_bucket, s3_object_name)

    print(result)

    #result = s3_client.upload_file(local_json_path, output_bucket, s3_object_name)
    s3_processed_objects.append(local_json_path)

    return result

handler('a','s')