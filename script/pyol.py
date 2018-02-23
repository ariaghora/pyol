import argparse
import json
import glob
import os
import requests
from colorama import Fore, init

init(convert=True, autoreset=True)

description = 'Run the local python scripts with the power of remote server.'

parser = argparse.ArgumentParser(description=description)
subparsers = parser.add_subparsers(dest='sub_commands')

init = subparsers.add_parser('init', description='Initial project folder synchronization')

run = subparsers.add_parser('run', description='Run the corresponding script on the server')
run.add_argument('filename')

args = parser.parse_args()

def get_host():
    return json.loads(open('pyolconfig.json','r').read())['hostname']

def get_project_name():
    return json.loads(open('pyolconfig.json','r').read())['project_name']

def upload(fn):
    url = get_host()+'/upload'
    files = {'file':open(fn, 'rb')}
    try:
        r = requests.post(url, files=files, data={'path':fn, 'project_name':get_project_name()})
    except:
        print('Operation failed. Please check if the server is running properly.')
        quit()

def delete_remote(fn):
    url = get_host()+'/delete'
    try:
        requests.post(url, data={'path':fn, 'project_name':get_project_name()})
    except:
        print('Operation failed. Please check if the server is running properly.')
        quit()

def execute_remote(fn):
    url = get_host()+'/execute'
    try:
        r = requests.post(url, data={'path':fn, 'project_name':get_project_name()})
        return r.text
    except:
        print('Operation failed. Please check if the server is running properly.')
        quit()
    return 'Execution failed.'

''' Synchronize project. Only sync modified files if "update" is set to true'''
def sync(update=True):
    def is_included(x):
        excluded_list = ['pyolconfig.json','pyolmeta.json']
        found = 0
        for i in excluded_list:
            if i in x: found+=1
        return found==0

    all_files = list(filter(lambda x:os.path.isfile(x), glob.glob('./**', recursive=True)))
    considered = list(filter(is_included, all_files))

    try:meta = json.loads(open('pyolmeta.json', 'r').read())
    except:meta={}

    for fn in considered:
        f = fn.replace('\\', '/')
        if not update:
            meta[f] = os.path.getmtime(f)
            print('Processing %s'%f)
            upload(f)
        else:
            # creation found
            if not f in meta:
                print(Fore.GREEN+'"%s" was created. Updating...'%f)
                meta[f] = os.path.getmtime(f)
                upload(f)

            # modification found 
            if meta[f] != os.path.getmtime(f):
                print(Fore.YELLOW+'"%s" has been modified. Updating...'%f)
                meta[f] = os.path.getmtime(f)
                upload(f)

    # deletion found
    meta_files = list(meta.keys())
    for k in meta_files:
        if not os.path.isfile(k):
            print(Fore.RED+'"%s" was deleted. Updating...'%k)
            delete_remote(k)
            meta.pop(k, None)

    with open('pyolmeta.json', 'w') as out:
        json.dump(meta, out)

def _init():
    project_name = input('Enter the project name: ')
    hostname = input('Enter the pyol server host: ')
    config = {
                'project_name':project_name,
                'hostname':hostname,
            }
    with open('pyolconfig.json', 'w') as out:
        json.dump(config, out)

    print('Synchronizing project files...')
    sync(update=False)
    print('Done.')

if args.sub_commands == 'init':
    _init()

if args.sub_commands == 'run':
    print('Checking if any modifications have been made...')
    sync(update=True)

    filename = args.filename

    print('Executing %s...'%filename)
    print('Output:\n')
    print(execute_remote(filename))

