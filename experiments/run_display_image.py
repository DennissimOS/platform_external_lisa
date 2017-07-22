#!/usr/bin/env python

import logging

from conf import LisaLogging
LisaLogging.setup()
import json
import os
import devlib
from env import TestEnv
from android import Screen, Workload, System
from trace import Trace
import trappy
import pandas as pd
import sqlite3
import argparse
import shutil

parser = argparse.ArgumentParser(description='DisplayImage tests')

parser.add_argument('--out_prefix', dest='out_prefix', action='store', default='default',
                    help='prefix for out directory')

parser.add_argument('--collect', dest='collect', action='store', default='energy',
                    help='What to collect (default energy). Also supports option '
                    'display-energy which suspends the cpu to help prevent extra '
                    'energy consumption by the cpu.')

parser.add_argument('--brightness', dest='brightness', action='store', default=100,
                    type=int,
                    help='Brightness of screen (default 100)')

parser.add_argument('--duration', dest='duration_s', action='store',
                    default=15, type=int,
                    help='Duration of test (default 15s)')

parser.add_argument('--serial', dest='serial', action='store',
                    help='Serial number of device to test')

args = parser.parse_args()

def experiment():
    # Get workload
    wload = Workload.getInstance(te, 'DisplayImage')

    outdir=te.res_dir + '_' + args.out_prefix
    try:
        shutil.rmtree(outdir)
    except:
        print "couldn't remove " + outdir
        pass
    os.makedirs(outdir)

    # Run DisplayImage
    wload.run(outdir, duration_s=args.duration_s, brightness=args.brightness,
            filepath=os.path.realpath('experiments/data/image.png'), collect=args.collect)

    # Dump platform descriptor
    te.platform_dump(te.res_dir)

    te._log.info('RESULTS are in out directory: {}'.format(outdir))

# Setup target configuration
my_conf = {

    # Target platform and board
    "platform"     : 'android',

    # Useful for reading names of little/big cluster
    # and energy model info, its device specific and use
    # only if needed for analysis
    # "board"        : 'pixel',

    # Device
    # By default the device connected is detected, but if more than 1
    # device, override the following to get a specific device.
    # "device"       : "HT6880200489",

    # Folder where all the results will be collected
    "results_dir" : "DisplayImage",

    # Define devlib modules to load
    "modules"     : [ ],

    "emeter" : {
        'instrument': 'monsoon',
        'conf': { }
    },

    # Tools required by the experiments
    "tools"   : [ ],
}

if args.serial:
    my_conf["device"] = args.serial

# Initialize a test environment using:
te = TestEnv(my_conf, wipe=False)
target = te.target

results = experiment()