import os
#from awpy import DemoParser
from operators.demoparser import DemoParser
import json

def demo_parse():
   
    NOTEBOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(NOTEBOOKS_DIR)
    DEMOS_DIR = os.path.join(BASE_DIR, "dags")

    demofile = os.path.join(DEMOS_DIR, "demo.dem")
    print(demofile)
    demo_parser = DemoParser(demofile=demofile, demo_id="demos3-parsed-teste_parse", parse_rate=128)

    demo_parser.parse()
    outfile = "demos3-parsed-teste_parse"
    with open(f'{outfile}.json') as json_file:
        data = json.load(json_file)
    print('data')
    #print('data is',data)

demo_parse()