import subprocess
import threading
import queue
import sys

STDOUT_TIMEOUT = 1

def read_stdout(proc, output_queue):
    for line in iter(proc.stdout.readline, ''):
        output_queue.put(line)
    proc.stdout.close()


def main():
    rng_proc = subprocess.Popen(['python', 'program_a.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    output_queue = queue.Queue()
    threading.Thread(target=read_stdout, args=(rng_proc, output_queue), daemon=True).start()

    try:
        while True:
            message_to_b = input("Enter a command: ")

            rng_proc.stdin.write(message_to_b + '\n')
            rng_proc.stdin.flush()

            try:
                response_from_b = output_queue.get(timeout=STDOUT_TIMEOUT).strip()
                print(f"Response:\n{response_from_b}")
            except queue.Empty:
                # print("Timeout. No response from program A.")
                continue # ignore

            if message_to_b.lower() == 'shutdown':
                print("Shutting down.")
                break

    finally:
        # Close communication
        rng_proc.stdin.close()
        rng_proc.wait()

if __name__ == "__main__":
    main()