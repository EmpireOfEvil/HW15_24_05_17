import os
from collections import namedtuple
import logging
import argparse

parser = argparse.ArgumentParser(description='Directory checker')
parser.add_argument('-address', type=str, help='target directory', default = '')
args = parser.parse_args()

logging.basicConfig(filename='logger.log', level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')

def grab_the_dir_data(parent: str = '') -> dict:
    datalist = []
    datapoint = namedtuple('datapoint', ['name', 'ext', 'isdir', 'parent'])

    for f in os.listdir():
        dp = datapoint(name = f, ext = None, isdir = os.path.isdir(f), parent = parent)
        if len(f.split('.')) > 1:
            dp = dp._replace(name = f.split('.')[0], ext = f.split('.')[-1])

        datalist.append(dp)
        logging.info(dp)
        
        if os.path.isdir(f):
            os.chdir(f)
            datalist += (grab_the_dir_data(f))
            os.chdir('..')
    return datalist

workdir = args.address if args.address else os.getcwd()
if not os.path.exists(workdir):
    logging.warning(f'SELECTED DIR {workdir} DOES NOT EXIST')
else:
    os.chdir(workdir)
    grab_the_dir_data(os.path.basename(workdir))