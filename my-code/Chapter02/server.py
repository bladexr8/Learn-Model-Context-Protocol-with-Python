# STDIO Server
import sys
import json

from utils.messages import initializeResponse

initialized = False

def send_response(response):
    print(json.dumps(response))
    sys.stdout.flush()

while True:
    for line in sys.stdin:
        message = line.strip()
        if message == "hello":
            send_response("hello there")
        elif message.startswith('{"jsonrpc":'):
            json_message = json.loads(message)
            method = json_message.get('method', '')

            # connection not initialized
            if not initialized:
                if method != "initialize" and method != "notifications/initialized":
                    print(f"Server not initialized. Please send an 'initialized' notification first. You sent {method}")
                    sys.stdout.flush()
                    continue

            match method:
                case "notifications/initialized":
                    # print("Server initialized successfully")
                    sys.stdout.flush()
                    initialized = True
                    break
                case "initialize":
                    print(json.dumps(initializeResponse))
                    sys.stdout.flush()
                    # initialized = True
                    break
                    # should return capabilities
                case "tools/list":
                    response = {
                        "jsonrpc": "2.0",
                        "id": json_message["id"],
                        "result": ["tool1","tool2"]
                    }
                    send_response(response)
                    break
                case _:
                    send_response(f"Unknown method: {json_message['method']}")
                    break
        elif message == "exit":
            send_response("Exiting server...")
            sys.exit(0)
        else:
            send_response(f"Unknown message: {message}")