import sys
import random

def process_message(message):
    COMMANDS = {
        "Hi": "Hi",
        "GetRandom": random.randint(1, 100_000),
        "Shutdown": "shutdown"
    }
    
    return COMMANDS.get(message, "")

def send_message(message = ""):
    if message == "":
        return
    
    sys.stdout.write(message + '\n')
    sys.stdout.flush()

def main():
    while True:
        message_from_a = sys.stdin.readline().strip()
        response = process_message(message_from_a)
        send_message(response)

        if message_from_a == "Shutdown":
            send_message("Program A: Shutting down.")
            break


if __name__ == "__main__":
    main()