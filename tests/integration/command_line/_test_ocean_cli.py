#!/usr/bin/env python
"""

    Tests for `ocean CLI`.

"""
#import unittest
#import random
import os
import os.path
import sys
import subprocess
import re
# import logging

# from pytest import (
#     mark,
#     raises,
# )

def test_ocean_cli():
    log_msg = 'Using default logging settings.'
    header = 'Index     Account                                             Ocean Tokens                                   Ether'
    program = sys.argv[0]
    if program[0] != '/':
        program = os.path.join(os.getcwd(), program)

    # fix for running from the command line 'python -m pytest tests' within venv
    if re.search(r'/venv/', program):
        program = './'

    pdir = os.path.normpath(os.path.dirname(program))
    dot_tox = pdir.find('/.tox')
    if dot_tox > 0:
        pdir = pdir[0:dot_tox]
    cli_path = os.path.join(pdir, "ocean")
    command = "balance"
    args = [cli_path, '--config', 'tests/resources/config.ini', command]
    cli = subprocess.run(args, stdout=subprocess.PIPE)
    stdout = cli.stdout.decode()
    assert 0 == cli.returncode
    lines = stdout.split('\n')
    print(lines)
    num_accounts = 3
    assert (num_accounts + 3) == len(lines)
    if len(lines) == (num_accounts + 3):
        assert log_msg == lines[0]
        assert header == lines[1]
        for i in range(num_accounts):
            account = lines[i + 2].split()
            assert 4 == len(account)
        last_account_id = account[1]
        # FUTURE assert valid_id(last_account_id)
        assert 0 == len(lines[num_accounts + 2])
    # test with narrowing to just one account
    args.append(last_account_id)
    cli = subprocess.run(args, stdout=subprocess.PIPE)
    stdout = cli.stdout.decode()
    assert 0 == cli.returncode
    lines = stdout.split('\n')
    num_accounts = 1
    assert (num_accounts + 3) == len(lines)
    if len(lines) == (num_accounts + 3):
        assert log_msg == lines[0]
        assert header == lines[1]
        for i in range(num_accounts):
            account = lines[i + 2].split()
            assert 4 == len(account)
        last_account_id2 = account[1]
        # FUTURE assert valid_id(last_account_id2)
        assert 0 == len(lines[num_accounts + 2])
    assert last_account_id == last_account_id2
