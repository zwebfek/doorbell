import alsaaudio, time, audioop, json, sys, requests

if len(sys.argv) > 1 and sys.argv[1].isdigit():
    min_val = int(sys.argv[1]) or 3000
else:
    min_val = 3000

print('min_val: ' + str(min_val))

with open('./config.json') as f:
    config = json.loads(f.read())

def send_message(api_key=config['telegram_bot_api_key'], chat_id=config['chat_id'], msg=config['message'], parse_mode='Markdown'):
    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode={}&text={}'.format(api_key, chat_id, parse_mode, msg)
    r = requests.get(url)
    return r.ok

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, device='hw:0,0')

# Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# Each frame is 2 bytes long.
# The reads below will return either 320 bytes or 0 bytes of data.
inp.setperiodsize(160)

print('Capturing audio...')

while True:
    l, data = inp.read()
    if l:
        # Return the maximum of the absolute value of all samples in a fragment.
        m = audioop.max(data, 2)
        if m >= min_val:
            print(m)
            print('min_val reached.')
            print('Sending message...')
            send_message()
            print('Message sent.')
            print('Quitting...')
            break
    time.sleep(.001)