# import os
# from parser.demoparser import DemoParser

# def demo_parse():

#     NOTEBOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
#     BASE_DIR = os.path.dirname(NOTEBOOKS_DIR)
#     DEMOS_DIR = os.path.join(BASE_DIR, "dags")

#     demofile = os.path.join(DEMOS_DIR, "demo.dem")
#     print(demofile)
#     demo_parser = DemoParser(demofile=demofile, demo_id="demos-parsed-teste_parse", parse_rate=128)

#     demo_parser.parse()

#     # demofile = 'demo.dem'
#     # demo_parser = DemoParser(demofile=demofile, demo_id="demos-parsed/teste_parse", parse_rate=128)

#     # demo_parser.parse()

# demo_parse()