#!/usr/bin/env python3
"""


    Build artifact library


"""

import argparse
import gzip
import json
import os
import re

DEFAULT_ARTICLE_LIBRARY = 'artifacts.json.gz'
DEFAULT_COMMAND = 'create'


def import_artifact_file(filename, data):
    if isinstance(filename, (list, tuple)):
        for file_item in filename:
            import_artifact_file(file_item, data)
        return

    if not os.path.exists(filename):
        print(f'{filename} does not exists')
    data_json = None
    with open(filename, 'r') as fp:
        data_json = json.load(fp)
    match = re.search(r'\W(\w+)\Wjson', filename)
    if match:
        network_name = match.group(1)

    contract_name = data_json['name']
    if network_name not in data:
        data[network_name] = {}

    data[network_name][contract_name] = data_json
    print(f'Adding {network_name}/{contract_name}')


def outptut_as_python_file(filename, data):
    with open(filename, 'w') as fp:
        fp.write('# auto generated artifle files\n')
        fp.write('artifact_data = {\n',)
        for network_name, item in data.items():
            fp.write(f"    '{network_name}': {{ \n")
            for contract_name, abi_item in item.items():
                fp.write(f"        '{contract_name}': {{\n")
                fp.write(f"            {abi_item},\n")
                fp.write('        }\n')

            fp.write('    }\n')
        fp.write('\n')


def output_as_json_file(filename, data, is_compressed):
    if is_compressed:
        with gzip.open(filename, 'wt') as fp:
            json.dump(data, fp)
    else:
        with open(filename, 'w') as fp:
            json.dump(data, fp)


def list_artifact_data(data):
    print(f'Network Name         Contract Name')
    for network_name, contract_names in data.items():
        for contract_name, item in contract_names.items():
            print(f'{network_name:20} {contract_name}')


def main():

    parser = argparse.ArgumentParser(description='Contract Artifact Library Builder')

    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help=f'Debug mode on or off, default: off',
    )

    parser.add_argument(
        '-u',
        '--update',
        action='store_true',
        help=f'Update the output file'
    )

    parser.add_argument(
        '-f',
        '--file',
        default=DEFAULT_ARTICLE_LIBRARY,
        help=f'filename of the artifact library filename to manage. Default: {DEFAULT_ARTICLE_LIBRARY}'
    )

    parser.add_argument(
        'command',
        default=DEFAULT_COMMAND,
        help='''command to execute, can be the following

            create or c - create a new artifact library. Default option
            udpate or u - update a current library
            list or l   - list the contents of a library

            '''
    )

    parser.add_argument(
        'artifact_filename',
        metavar='artifact-file',
        nargs='?',
        help='input abi filename'
    )
    args = parser.parse_args()

    library_file = args.file
    if re.search(r'\.gz$', library_file):
        library_file_gz = library_file
        library_file = re.sub(r'\.gz$', '', library_file_gz)
    else:
        library_file_gz = f'{library_file}.gz'

    artifact_data = {}

    command_char = args.command.lower()[0]

    if os.path.exists(library_file) or os.path.exists(library_file_gz):
        if command_char == 'c':
            print(f'You cannot create an existing library file "{library_file}"')
            return

        if os.path.exists(library_file_gz):
            with gzip.open(library_file_gz, 'rt') as fp:
                artifact_data = json.load(fp)

        if os.path.exists(library_file):
            with open(library_file, 'r') as fp:
                artifact_data = json.load(fp)

    if command_char == 'c' or command_char == 'u':
        if args.artifact_filename:
            import_artifact_file(args.artifact_filename, artifact_data)
            output_as_json_file(library_file_gz, artifact_data, True)
        else:
            print('Please provide a single or multiple contract article files to create/udpate to this library')

    elif command_char == 'l':
        list_artifact_data(artifact_data)
    else:
        print(f'Unknown command {args.command}')


if __name__ == "__main__":
    main()
