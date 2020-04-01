#!/usr/bin/env python3
"""


    Build artifact library


"""

import argparse
import base64
import json
import gzip
import re
import os


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
        for network_name, item in artifact_data.items():
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
        'output_filename',
        metavar='out-file',
        help='main artifact library filename to create/update'
    )

    parser.add_argument(
        'artifact_filename',
        metavar='artifact-file',
        nargs='+',
        help='input abi filename'
    )
    args = parser.parse_args()

    output_file = args.output_filename
    if re.search('\.gz$', output_file):
        output_file_gz = output_file
        output_file = re.sub('\.gz$', '', output_file_gz)
    else:
        output_file_gz = f'{output_file}.gz'

    artifact_data = {}

    if os.path.exists(output_file) or os.path.exists(output_file_gz):
        if not args.update:
            print(f'The output file {output_file} already exists, please use the -u --update option to overwite this file')
            return

        if os.path.exists(output_file_gz):
            with gzip.open(output_file_gz, 'rt') as fp:
                artifact_data = json.load(fp)

        if os.path.exists(output_file):
            with open(output_file, 'r') as fp:
                artifact_data = json.load(fp)

    import_artifact_file(args.artifact_filename, artifact_data)

    output_as_json_file(output_file_gz, artifact_data, True)



if __name__ == "__main__":
    main()