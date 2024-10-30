import sys

while True:
    message_from_a = sys.stdin.readline().strip()

    if message_from_a.lower() == "shutdown":
        sys.stdout.write("Program B: Shutting down.\n")
        sys.stdout.flush()
        break

    sys.stdout.write(f"Program B received: {message_from_a}\n")
    sys.stdout.flush()
