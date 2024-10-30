import sys
import random

MAX_RANDOM_NUMBER = 100_000

def process_message(message):
    COMMANDS = {
        "Hi": "Hi",
        "GetRandom": random.randint(1, MAX_RANDOM_NUMBER),
        "Shutdown": "shutdown"
    }
    
    return COMMANDS.get(message, "")

def send_message(message = ""):
    if message == "":
        return
    
    sys.stdout.write(str(message) + '\n')
    sys.stdout.flush()

def main():
    while True:
        message_from_controller = sys.stdin.readline().strip()
        response = process_message(message_from_controller)
        send_message(response)

        if message_from_controller == "Shutdown":
            send_message("Program A: Shutting down.")
            break


if __name__ == "__main__":
    main()