# send.py
# simulates a remote Pi client
# sends a message to the server when run
import requests
import json
import sys

if len(sys.argv) < 3:
    print("Please enter a message like so:\n\npy send.py <Channel number> Hello World")
    sys.exit(1)
try:
    channel = int(sys.argv[1])
    if channel < 0:
        raise ValueError
except ValueError:
    print("Please enter a valid channel number")

# get message from comman line args
text = ''
for arg in sys.argv[2:]:
    text += arg + ' '
text = text[:-1]

# set up data values for the HTTP request
url = "http://localhost:3001"
data = {'sender': 'Remote User', 'text': text, 'channel': channel}
headers = {'Content-type': 'application/json'}
# send the requesta and print the result
print(requests.post(url, data = json.dumps(data), headers=headers))