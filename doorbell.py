#!/usr/bin/env python

import alsaaudio, requests, os, time, audioop, json, sys, optparse

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
    parser.add_option("-t", "--trigger-val", type="int", dest="trigger_val", help="set volume trigger level")
    parser.add_option("-d", "--device", type="string", dest="device", help="set audio device that will be listened on")
    parser.add_option("-m", "--message", type="string", dest="message", help="set message that will be sent")
    parser.add_option("-k", "--telegram-api-key", type="string", dest="telegram_api_key", help="set telegram api key")
    parser.add_option("-c", "--chat-id", type="string", dest="chat_id", help="set id of the telegram chat that the message will be sent to")
    return parser.parse_args()

def send_message(telegram_api_key, chat_id, message, parse_mode="Markdown"):
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode={}&text={}"
    r = requests.get(url.format(telegram_api_key, chat_id, parse_mode, message))
    return r.ok

def listen_for_trigger(trigger_val=20000, device="hw:0,0"):
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, device=device)
    # Mono, 8000 Hz, 16 bit little endian samples
    inp.setchannels(1)
    inp.setrate(8000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(160)
    print("[+] Capturing audio...")
    while True:
        l, data = inp.read()
        if l:
            # Return the maximum of the absolute value of all samples in a fragment.
            m = audioop.max(data, 2)
            if m >= trigger_val:
                return True
        time.sleep(.001)

config = get_config()
(options, arguments) = get_arguments(config)
print("Trigger value = " + str(options.trigger_val))

if listen_for_trigger(trigger_val=options.trigger_val, device=options.device):
    print("[+] Trigger value reached.")
    print("[+] Sending message...")
    if send_message(options.telegram_api_key, options.chat_id, options.message):
        print("[+] Message sent.")