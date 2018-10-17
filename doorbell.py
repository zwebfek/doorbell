#!/usr/bin/env python

import os
import json
import optparse

def get_config(path="./config.json"):
    config = {}
    if os.path.exists(path):
        with open(path) as f:
            config = json.loads(f.read())
    config.setdefault('telegram_api_key', None)
    config.setdefault('chat_id', None)
    config.setdefault('trigger_val', 20000)
    config.setdefault('message', "Ding dong!")
    config.setdefault('device', "hw:0,0")
    return config

def get_arguments(config={}):
    parser = optparse.OptionParser()
    parser.set_defaults(**config)
    parser.add_option("-t", "--trigger-val", type="int", dest="trigger_val")
    parser.add_option("-d", "--device", type="string", dest="device")
    parser.add_option("-m", "--message", type="string", dest="message")
    parser.add_option("-k", "--telegram-api-key", type="string", dest="telegram_api_key")
    parser.add_option("-c", "--chat-id", type="string", dest="chat_id")
    return parser.parse_args()

config = get_config()
(options, arguments) = get_arguments(config)
print(options)
