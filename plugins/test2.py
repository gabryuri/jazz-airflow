import os
# from awpy import DemoParser
# from lightawpy.demoparser import DemoParser
from operators.demoparser import DemoParser
import json

def demo_parse():
   
    NOTEBOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(NOTEBOOKS_DIR)
    DEMOS_DIR = os.path.join(BASE_DIR, "dags")

    demofile = os.path.join(DEMOS_DIR, "demo.dem")
    print(demofile)
    demo_parser = DemoParser(demofile=demofile, demo_id="demos4-parsed-teste_parse", parse_rate=128)

    parsed_result = demo_parser.parse()

    result = demo_parser.read_json
    print('parsed_result:', parsed_result['mapName'])
    #print(res)
    # outfile = "demos3-parsed-teste_parse"
    # with open(f'{outfile}.json') as json_file:
    #     data = json.load(json_file)
    # print('data')
    #print('data is',data)


# def sprocess():
#     import subprocess


#     command = ['go', 'run', 'parse_demo.go',
#      '-demo', 'demo.dem',
#      '-parserate', '128', '-tradetime', '5',
#      '-buystyle', 'hltv', '-demoid',
#      'demozz', '-out', 'test',
#      '--parseframes']

#     print( (' ').join(command))
#     proc = subprocess.Popen(
#         command,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         #cwd='path'
#     )
#     process_output, second_output =  proc.communicate()

#     print(process_output, second_output)
#     with proc.stdout as f :
#         print(f.read())

# sprocess()
#demo_parse()