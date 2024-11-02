
# JetBrains_Project_2025

## Task Description

In this task, you will create two programs that interact with each other through standard input and output.

## How to run

The controller is `program_B.py`. It can run the programs ``program_A.py`` and ``program_A.kt``.

The programs should be passed as an argument to `program_B.py`.

Example:

```bash
python3 program_B.py program_A.py
```

or

```bash
python3 program_B.py program_A.kt
```

For Kotlin support (compilation and program running), `kotlinc` and `Java` are required to be installed on the system, and added to `PATH`.
I've installed them via [Chocolatey]("https://chocolatey.org/install").

## How to debug

In `program_B.py`, you need to change the `DEBUG` value (line 9) from `False` to `True`. This way, you can send custom messages to the `program_A` via the Controller.


## Program A: Pseudo-Random Number Generator


Program A will act as a pseudo-random number generator. It reads commands from stdin, where each command is delimited by a line break, and writes responses to stdout. The program should handle the following commands:


-  **Hi**: Responds with "Hi" on stdout.

-  **GetRandom**: Responds with a pseudo-random integer on stdout.

-  **Shutdown**: Gracefully terminates the program.

Any unknown commands should be ignored.


## Program B: Controller


Program B will launch Program A as a separate process, provided as an argument. Once Program A is running, Program B should:
  

- Send the Hi command to Program A and verify the correct response.

- Retrieve 100 random numbers by sending the GetRandom command to Program A 100 times.

- Send the Shutdown command to Program A to terminate it gracefully.

- Sort the list of retrieved random numbers and print the sorted list to the console.

- Calculate and print the median and average of the numbers.