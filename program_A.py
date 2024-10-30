import subprocess

proc_b = subprocess.Popen(['python3', 'program_b.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

try:
    while True:
        message_to_b = input("Program A: Enter a message: ")

        proc_b.stdin.write(message_to_b + '\n')
        proc_b.stdin.flush()

        response_from_b = proc_b.stdout.readline().strip()
        print(f"Program A received:\n{response_from_b}")

        if message_to_b.lower() == 'shutdown':
            print("Program A: Shutting down.")
            break

finally:
    # Close communication
    proc_b.stdin.close()
    proc_b.stdout.close()
    proc_b.wait()
