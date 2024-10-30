import subprocess
import threading
import queue
import sys
import os

STDOUT_TIMEOUT = 1
DEBUG = False

def read_stdout(proc, output_queue):
    for line in iter(proc.stdout.readline, ''):
        output_queue.put(line)
    proc.stdout.close()

def start_process(program_name):
    if not os.path.exists(str(program_name)):
        print(f"Program {program_name} does not exist.")
        return None, None
   
    if program_name.endswith('.kt'):
        print("Compiling Kotlin program...")
        compile_proc = subprocess.run(['kotlinc', program_name, '-include-runtime', '-d', 'program_A.jar'])
        
        if compile_proc.returncode != 0:
            print(f"Failed to compile {program_name}")
            return None, None
        
        print("Kotlin program compiled successfully.")
        proc = subprocess.Popen(['java', '-jar', 'program_A.jar'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    
    elif program_name.endswith('.py'):
        proc = subprocess.Popen(['python', program_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    
    elif program_name.endswith('.jar'):
        proc = subprocess.Popen(['java', '-jar', program_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    
    else:
        print(f"Unsupported file type: {program_name}")
        return None, None
    
    output_queue = queue.Queue()
    threading.Thread(target=read_stdout, args=(proc, output_queue), daemon=True).start()

    return proc, output_queue

class Controller:
    def __init__(self, program_name=None):
        self.program_name = program_name
        self.rng_proc, self.output_queue = start_process(program_name)
        
        if self.rng_proc is None:
            sys.exit(1)

    def get_response(self):
        try:
            rng_response = self.output_queue.get(timeout=STDOUT_TIMEOUT).strip()
            return rng_response
        except queue.Empty:
            # Timeout, RNG did not respond
            return None
        
    def send_command(self, command):
        self.rng_proc.stdin.write(command + '\n')
        self.rng_proc.stdin.flush()
        
        return self.get_response()
    
def main():
    controller = Controller('program_a.py')
    # controller = Controller('program_a.kt')
    # controller = Controller('program_a.jar')
    
    random_numbers = []
    
    ping_response = controller.send_command("Hi")
    if ping_response != "Hi":
        print("Program A did not respond correctly.")
        controller.send_command("Shutdown")
        return
    
    for _ in range(100):
        number = controller.send_command("GetRandom")
        random_numbers.append(int(number))
        
    controller.send_command("Shutdown")
    
    # Doing the work
    random_numbers.sort()
    print(f"Sorted random numbers: {random_numbers}")
    
    if len(random_numbers) % 2 == 0:
        median = (random_numbers[len(random_numbers) // 2 - 1] + random_numbers[len(random_numbers) // 2]) / 2
    else:
        median = random_numbers[len(random_numbers) // 2]
    print(f"Median: {median}")

def debug():
    PROGRAMS = {
        "1": "program_a.py",
        "2": "program_a.kt",
        "3": "program_a.jar"
    }
    
    while True:
        print("Debug mode:")
        print("""Select a program to run:
        1. program_a.py
        2. program_a.kt
        3. program_a.jar
        4. Custom program name
        5. Exit
            """)
        
        choice = input("Enter your choice: ")
        if choice == '5':
            print("Exiting.")
            return
        
        elif choice == '4':
            program_name = input("Enter the program name: ")
            controller = Controller(program_name)
            break
            
        elif choice in PROGRAMS:
            program_name = PROGRAMS.get(choice)
            controller = Controller(program_name)
            break
            
        else:
            print("Invalid choice.")
            continue
        
    # controller = Controller('program_a.py')
    # controller = Controller('program_a.kt')
    # controller = Controller('program_a.jar')
    
    print("Running " + controller.program_name)
    print("Available commands: Hi, GetRandom, Shutdown")
    while True:
        command = input("Enter a command: ")
        response = controller.send_command(command)
        print(f"Response:\n{response}")
        
        if command == 'Shutdown':
            print("Shutting down.")
            break

def _test():
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
    if DEBUG:
        debug()
    else:
        main()