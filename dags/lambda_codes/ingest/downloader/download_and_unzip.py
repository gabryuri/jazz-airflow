import os
import requests 




def lambda_handler(event, context):
    match_id = 71821
    DEMOS_COMPRESSED_DIR = 'tmp'
    url=f'https://www.hltv.org/download/demo/{str(match_id)}'
    
   
    resp = requests.get(url)

    # assuming the subdirectory tempdata has been created:
    zname = os.path.join(DEMOS_COMPRESSED_DIR, "test_demos.rar")
    zfile = open(zname, 'wb')
    zfile.write(resp.content)
    zfile.close()

    extract('test_demos',DEMOS_COMPRESSED_DIR)


def extract(demo_file, DEMOS_COMPRESSED_DIR):
    demo_file = os.path.join(DEMOS_COMPRESSED_DIR, 'test_demos')
    os.system(f'unrar x {demo_file}.rar {DEMOS_COMPRESSED_DIR}')
    return None


lambda_handler('','')