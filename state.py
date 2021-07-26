#!/usr/bin/env python3

import sys
# for terraform mv command
import os

def fetch_modules(filename):
    with open(filename,'r') as tf_file:
        lines = tf_file.readlines()
        module_name = None
        subscription_name = None
        in_module = False # State logic. If True, we are inside of the module
        for line in lines:
            if line.startswith('module '):
                module_name = line.split(' ')[1][1:-1] # Second element of a list and slice everything else
                in_module = True
            elif line[0] == '}':
                if in_module:
                    in_module = False
                    if not subscription_name is None: # Check absence of the subscription_name
                        yield((module_name,subscription_name))
                        subscription_name = None # Return both values, zeroing sub
            else:
                # Generate list of two elems with = delemiter
                parts = [x.strip() for x in line.split('=')]
                if len(parts) == 2:
                    expr_name,expression = parts
                    if expr_name == 'subscription_name':
                        subscription_name = expression[1:-1]


get_subscription_name = lambda module_name,subscription_name: \
    'module.' + module_name + '.google_pubsub_subscription.subscription[0] ' + \
    'module.' + module_name + '.google_pubsub_subscription.subscription["'+ subscription_name + '"]'

def do_fetch_modules(filename):
    for module_name,subscription_name in fetch_modules(filename):
        #os.system('terraform state mv ' + get_subscription_name(module_name,subscription_name))
        print(get_subscription_name(module_name,subscription_name))

if __name__ == '__main__':
    do_fetch_modules(sys.argv[1])