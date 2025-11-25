import subprocess
import json

from utils.messages import list_tools_message, initialize_message, initialized_message

# start the child process
proc = subprocess.Popen(
    ['python3', 'server.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

list_tools_message = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
};

message = 'hello\n'


def send_message(message):
    """Send a message to the child process"""
    print(f'[CLIENT] Sending message to server... Message: {message.strip()}')
    proc.stdin.write(message)
    proc.stdin.flush()

def serialize_message(message):
    """Serialize a message to JSON format"""
    return json.dumps(message) + '\n'

def print_response(response, prefix = ""):
    """Print the response from the server."""
    try:
        parsed = json.loads(response)
        print(prefix,json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print(prefix, response.strip())

def connect():
    print("Connecting to MCP Server...")
    
    # 1. Ask for capabilities
    send_message(serialize_message(initialize_message))
    # Read response from child/server
    response = proc.stdout.readline()
    print_response(response, prefix='[SERVER]: \n')

    # 2. Send initialized notification, handshake is done
    send_message(serialize_message(initialized_message))

def list_tools():
    # 3. send a message to list tools
    # send a JSON-RPC message
    send_message(serialize_message(list_tools_message))
    response = proc.stdout.readline()
    print_response(response, prefix='[SERVER]: \n')

def close_server():
    # this closes down the child aka server
    send_message('exit\n')

    proc.stdin.close()
    exit_code = proc.wait()
    print(f"Child exited with code {exit_code}")

def main():
    connect()
    list_tools()
    close_server()

main()
