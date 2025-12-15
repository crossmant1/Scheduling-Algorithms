import random
from collections import deque


processes = [
    {'pID': 1, 'burst_time': random.randrange(1, 10), 'arrival_time': random.randrange(0, 10)},
    {'pID': 2, 'burst_time': random.randrange(1, 10), 'arrival_time': random.randrange(0, 10)},
    {'pID': 3, 'burst_time': random.randrange(1, 10), 'arrival_time': random.randrange(0, 10)}
]

# First Come First Serve -----------------------------------------------------------------------------------------------
first_arrived, second_arrived, third_arrived = sorted(processes, key=lambda p: p['arrival_time']) # assign processes to the order they arrived

first_arrived_start_time=first_arrived['arrival_time']

if((first_arrived['arrival_time']+first_arrived['burst_time'])<second_arrived['arrival_time']): # detects if there is a gap between the first's completion time and second's arrival time
    second_arrived_start_time=second_arrived['arrival_time']
else:
    second_arrived_start_time=(first_arrived['arrival_time']+first_arrived['burst_time'])

if(second_arrived_start_time+second_arrived['burst_time']<third_arrived['arrival_time']):# detects if there is a gap between the second's completion time and third's arrival time
    third_arrived_start_time=third_arrived['arrival_time']
else:
    third_arrived_start_time=second_arrived_start_time+second_arrived['burst_time']

second_arrived_wait_time=second_arrived_start_time-second_arrived['arrival_time'] # wait time is time between the process's start time and arrival time
third_arrived_wait_time=third_arrived_start_time-third_arrived['arrival_time']

first_arrived_completion_time = first_arrived_start_time + first_arrived['burst_time'] # their completion time is when they started plus their burst time
second_arrived_completion_time = second_arrived_start_time + second_arrived['burst_time']
third_arrived_completion_time = third_arrived_start_time + third_arrived['burst_time']

first_arrived_TAT=first_arrived_completion_time-first_arrived['arrival_time'] # Turnaround time is difference between completion time and arrival time.
second_arrived_TAT=second_arrived_completion_time-second_arrived['arrival_time']
third_arrived_TAT=third_arrived_completion_time-third_arrived['arrival_time']

average_waiting_time=(0+second_arrived_wait_time+third_arrived_wait_time)/3
average_TAT=(first_arrived_TAT+second_arrived_TAT+third_arrived_TAT)/3
throughput=3/(third_arrived_completion_time-first_arrived_start_time)

print("For First Come First Serve:\n")

print(f"Process {first_arrived['pID']}: Arrival time: {first_arrived['arrival_time']}, "
      f"Burst time: {first_arrived['burst_time']}, "
      f"Start time: {first_arrived_start_time}, "
      f"Completion time: {first_arrived_completion_time}, "
      f"Wait time: 0, "
      f"Turnaround time: {first_arrived_TAT}\n")

print(f"Process {second_arrived['pID']}: Arrival time: {second_arrived['arrival_time']}, "
      f"Burst time: {second_arrived['burst_time']}, "
      f"Start time: {second_arrived_start_time}, "
      f"Completion time: {second_arrived_completion_time}, "
      f"Wait time: {second_arrived_wait_time}, "
      f"Turnaround time: {second_arrived_TAT}\n")

print(f"Process {third_arrived['pID']}: Arrival time: {third_arrived['arrival_time']}, "
      f"Burst time: {third_arrived['burst_time']}, "
      f"Start time: {third_arrived_start_time}, "
      f"Completion time: {third_arrived_completion_time}, "
      f"Wait time: {third_arrived_wait_time}, "
      f"Turnaround time: {third_arrived_TAT}\n")

print(f"Average Waiting Time: {average_waiting_time:.2f}")
print(f"Average Turnaround Time: {average_TAT:.2f}")
print(f"Throughput: {throughput:.2f} processes per unit time")

# Round Robin, time_quantum= 5 -----------------------------------------------------------------------------------------

for p in processes:#include remaining time
    p['remaining_time'] = p['burst_time']

processes.sort(key=lambda p: p['arrival_time'])#sort by arrival time

time_quantum=5
ready_queue = deque()
completed_processes = []
current_time = 0
process_index = 0
n = len(processes)


while len(completed_processes) < n:
    while process_index < n and processes[process_index]['arrival_time'] <= current_time: # add new process to the queue
        ready_queue.append(processes[process_index])
        process_index += 1

    if not ready_queue:
        if process_index < n:
            current_time = processes[process_index]['arrival_time']
        continue

    # Get the next process from the front of the queue
    current_process = ready_queue.popleft()

    # Determine how long this process will run (either the full quantum or its remaining time)
    run_time = min(time_quantum, current_process['remaining_time'])

    current_time += run_time
    current_process['remaining_time'] -= run_time

    while process_index < n and processes[process_index]['arrival_time'] <= current_time:#check for new processes
        ready_queue.append(processes[process_index])
        process_index += 1

    if current_process['remaining_time'] == 0:# if it is finished, calculate the completion, TAT, and wait times.

        current_process['completion_time'] = current_time
        current_process['turnaround_time'] = current_process['completion_time'] - current_process['arrival_time']
        current_process['wait_time'] = current_process['turnaround_time'] - current_process['burst_time']
        completed_processes.append(current_process)
    else:
        ready_queue.append(current_process) #if the process is not finished, add it back to the ready queue.


total_wait_time = sum(p['wait_time'] for p in completed_processes)
total_turnaround_time = sum(p['turnaround_time'] for p in completed_processes)

average_waiting_time = total_wait_time / n
average_TAT = total_turnaround_time / n

first_arrival = min(p['arrival_time'] for p in completed_processes)
last_completion = max(p['completion_time'] for p in completed_processes)
throughput = n / (last_completion - first_arrival)

# Sort by pID for a clean final display
completed_processes.sort(key=lambda p: p['pID'])
p1, p2, p3 = completed_processes

print("\nFor Round Robin. time_quantum = 5:\n")

print(f"Process {p1['pID']}: Arrival time: {p1['arrival_time']}, "
      f"Burst time: {p1['burst_time']}, "
      f"Completion time: {p1['completion_time']}, "
      f"Wait time: {p1['wait_time']}, "
      f"Turnaround time: {p1['turnaround_time']}\n")

print(f"Process {p2['pID']}: Arrival time: {p2['arrival_time']}, "
      f"Burst time: {p2['burst_time']}, "
      f"Completion time: {p2['completion_time']}, "
      f"Wait time: {p2['wait_time']}, "
      f"Turnaround time: {p2['turnaround_time']}\n")

print(f"Process {p3['pID']}: Arrival time: {p3['arrival_time']}, "
      f"Burst time: {p3['burst_time']}, "
      f"Completion time: {p3['completion_time']}, "
      f"Wait time: {p3['wait_time']}, "
      f"Turnaround time: {p3['turnaround_time']}\n")

print(f"Average Waiting Time: {average_waiting_time:.2f}")
print(f"Average Turnaround Time: {average_TAT:.2f}")
print(f"Throughput: {throughput:.2f} processes per unit time")


# Round Robin, time_quantum= 10 ----------------------------------------------------------------------------------------

for p in processes:#include remaining time
    p['remaining_time'] = p['burst_time']

processes.sort(key=lambda p: p['arrival_time'])#sort by arrival time

time_quantum=10
ready_queue = deque()
completed_processes = []
current_time = 0
process_index = 0
n = len(processes)


while len(completed_processes) < n:
    while process_index < n and processes[process_index]['arrival_time'] <= current_time: # add new process to the queue
        ready_queue.append(processes[process_index])
        process_index += 1

    if not ready_queue:
        if process_index < n:
            current_time = processes[process_index]['arrival_time']
        continue

    current_process = ready_queue.popleft() # get the next process from the front of the queue

    run_time = min(time_quantum, current_process['remaining_time'])#Determine how long this process will run

    current_time += run_time
    current_process['remaining_time'] -= run_time

    while process_index < n and processes[process_index]['arrival_time'] <= current_time:#check for new processes
        ready_queue.append(processes[process_index])
        process_index += 1

    if current_process['remaining_time'] == 0:# if it is finished, calculate the completion, TAT, and wait times.

        current_process['completion_time'] = current_time
        current_process['turnaround_time'] = current_process['completion_time'] - current_process['arrival_time']
        current_process['wait_time'] = current_process['turnaround_time'] - current_process['burst_time']
        completed_processes.append(current_process)
    else:
        ready_queue.append(current_process) #if the process is not finished, add it back to the ready queue.


total_wait_time = sum(p['wait_time'] for p in completed_processes)
total_turnaround_time = sum(p['turnaround_time'] for p in completed_processes)

average_waiting_time = total_wait_time / n
average_TAT = total_turnaround_time / n

first_arrival = min(p['arrival_time'] for p in completed_processes)
last_completion = max(p['completion_time'] for p in completed_processes)
throughput = n / (last_completion - first_arrival)

# Sort by pID for a clean final display
completed_processes.sort(key=lambda p: p['pID'])
p1, p2, p3 = completed_processes

print("\nFor Round Robin, time_quantum = 10:\n")

print(f"Process {p1['pID']}: Arrival time: {p1['arrival_time']}, "
      f"Burst time: {p1['burst_time']}, "
      f"Completion time: {p1['completion_time']}, "
      f"Wait time: {p1['wait_time']}, "
      f"Turnaround time: {p1['turnaround_time']}\n")

print(f"Process {p2['pID']}: Arrival time: {p2['arrival_time']}, "
      f"Burst time: {p2['burst_time']}, "
      f"Completion time: {p2['completion_time']}, "
      f"Wait time: {p2['wait_time']}, "
      f"Turnaround time: {p2['turnaround_time']}\n")

print(f"Process {p3['pID']}: Arrival time: {p3['arrival_time']}, "
      f"Burst time: {p3['burst_time']}, "
      f"Completion time: {p3['completion_time']}, "
      f"Wait time: {p3['wait_time']}, "
      f"Turnaround time: {p3['turnaround_time']}\n")

print(f"Average Waiting Time: {average_waiting_time:.2f}")
print(f"Average Turnaround Time: {average_TAT:.2f}")
print(f"Throughput: {throughput:.2f} processes per unit time")

# Shortest Job First ---------------------------------------------------------------------------------------------------
num_processes = len(processes)

process_queue = list(processes) #copy the list

completed_processes = []
current_time = 0
total_waiting_time = 0
total_turnaround_time = 0

while len(completed_processes) < num_processes: # loop to keep going until all processes are completed
    ready_queue = [p for p in process_queue if p['arrival_time'] <= current_time]

    if not ready_queue: #find the process with the earliest arrival time
        next_arrival_time = min(p['arrival_time'] for p in process_queue)
        current_time = next_arrival_time
        continue

    next_process = min(ready_queue, key=lambda p: p['burst_time'])# find the process with the shortest burst time

    # calculate times for the current process
    start_time = current_time
    completion_time = start_time + next_process['burst_time']
    turnaround_time = completion_time - next_process['arrival_time']
    waiting_time = turnaround_time - next_process['burst_time']

    total_waiting_time += waiting_time
    total_turnaround_time += turnaround_time

    # store the results
    next_process['start_time'] = start_time
    next_process['completion_time'] = completion_time
    next_process['waiting_time'] = waiting_time
    next_process['turnaround_time'] = turnaround_time

    # when the process finishes, move it to a completed list
    completed_processes.append(next_process)
    process_queue.remove(next_process)

    current_time = completion_time


average_waiting_time = total_waiting_time / num_processes
average_TAT = total_turnaround_time / num_processes

completed_processes.sort(key=lambda p: p['pID'])#sort the completed arrays

first_start_time = min(p['start_time'] for p in completed_processes)
last_completion_time = max(p['completion_time'] for p in completed_processes)
total_duration = last_completion_time - first_start_time
throughput = num_processes / total_duration

print("\nFor Shortest Job First:\n")

for p in completed_processes:
    print(f"pID: {p['pID']} | Arrival: {p['arrival_time']:<2} | Burst: {p['burst_time']:<2} | "
          f"Start: {p['start_time']:<2} | Completion: {p['completion_time']:<2} | "
          f"Wait: {p['waiting_time']:<2} | TAT: {p['turnaround_time']:<2}")


print(f"\nAverage Waiting Time:    {average_waiting_time:.2f}")
print(f"Average Turnaround Time: {average_TAT:.2f}")
print(f"Throughput:              {throughput:.2f} processes/unit time")


# Shortest Remaining Job First (Preemptive) ----------------------------------------------------------------------------
num_processes = len(processes)

process_queue = [] # create a queue to
for p in processes:
    p_copy = p.copy()
    p_copy['remaining_time'] = p_copy['burst_time']
    p_copy['start_time'] = -1  #use -1 to indicate not yet started
    process_queue.append(p_copy)

completed_processes = []
current_time = 0
total_waiting_time = 0
total_turnaround_time = 0

while len(completed_processes) < num_processes:
    ready_queue = [p for p in process_queue if p['arrival_time'] <= current_time] # put all the processes that have not been completed

    if not ready_queue:
        next_arrival_time = min(p['arrival_time'] for p in process_queue) # find the earliest arrival time
        current_time = next_arrival_time
        continue

    next_process = min(ready_queue, key=lambda p: p['remaining_time']) #select the process with the shortest remaining time

    if next_process['start_time'] == -1: # check to see if this is the process's first time running
        next_process['start_time'] = current_time

    next_process['remaining_time'] -= 1
    current_time += 1

    if next_process['remaining_time'] == 0: # check if process has been completed
        completion_time = current_time
        turnaround_time = completion_time - next_process['arrival_time']
        waiting_time = turnaround_time - next_process['burst_time']

        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time

        next_process['completion_time'] = completion_time
        next_process['waiting_time'] = waiting_time
        next_process['turnaround_time'] = turnaround_time

        completed_processes.append(next_process) # if the process is completed remove it from process queue.
        process_queue.remove(next_process)

average_waiting_time = total_waiting_time / num_processes
average_TAT = total_turnaround_time / num_processes

completed_processes.sort(key=lambda p: p['pID'])

first_start_time = min(p['start_time'] for p in completed_processes if p['start_time'] != -1)
last_completion_time = max(p['completion_time'] for p in completed_processes)
total_duration = last_completion_time - first_start_time
throughput = num_processes / total_duration if total_duration > 0 else 0

print("\nFor Shortest Job Remaining First (Preemptive):\n")

for p in completed_processes:
    print(f"pID: {p['pID']} | Arrival: {p['arrival_time']:<2} | Burst: {p['burst_time']:<2} | "
          f"Start: {p['start_time']:<2} | Completion: {p['completion_time']:<2} | "
          f"Wait: {p['waiting_time']:<2} | TAT: {p['turnaround_time']:<2}")


print(f"\nAverage Waiting Time:    {average_waiting_time:.2f}")
print(f"Average Turnaround Time: {average_TAT:.2f}")
print(f"Throughput:              {throughput:.2f} processes/unit time")

