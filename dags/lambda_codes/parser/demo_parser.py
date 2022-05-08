import json
import boto3

demo_path = ''
processed_folder = ''

landing_bucket = 'jazz-landing'
processed_bucket = 'jazz-processed'
def handler(event, context):

    #ti = kwargs['ti']
    #exec_date = kwargs['ds']

    #object_list = ti.xcom_pull(task_ids='scan_for_demos')

    s3_client = boto3.client('s3')

    s3_processed_objects = []

    object_list = ['pasta1/demo1.dem', 'pasta2/demo2.dem']

    for s3_object in object_list:
        print('PROCESSING FILE ', s3_object)
        
        demo_path = os.path.join(demos_folder, os.path.basename(s3_object))
        print('demo being saved to: ', demo_path)
        s3_client.download_file(landing_bucket, s3_object, demo_path)
        
        demo_name = os.path.basename(s3_object.strip('.dem'))
        print('demo name: ', demo_name)
        demo_parser = DemoParser(
            demofile=demo_path,
            demo_id=demo_name, 
            outpath=processed_folder,
            parse_rate=128)

        demo_parser.parse()

        local_json_path = os.path.join(processed_folder, demo_name)+".json"
        s3_object_name = os.path.join(exec_date, demo_name)+".json"

        s3_client.upload_file(local_json_path, output_bucket, s3_object_name)
        s3_processed_objects.append(local_json_path)

        #todo limpar os dados locais
    return s3_processed_objects