from reader import *
from tasker import *

import pandas as pd
import matplotlib.pyplot as plt


def plot_schedule_positions(schedules, schedule_report, plot_file: str) -> None:
    for i in range(len(schedules)):
        schedule = schedules[i]
        report = schedule_report[i]

        if report is None:
            continue

        df = pd.DataFrame(report, columns = ["time", "total", "distance", "battery"])
        plt.plot(df["time"], df["distance"], label = schedule["robot_id"])

    plt.xlabel("Time (hours)")
    plt.ylabel("Distance from origin (km)")
    plt.legend()
    plt.savefig(plot_file)

def write_feasibility_report(report_path:str, task_ids:list[dict], results:list[bool]) -> None:
    '''
        Description: Writes task feasibility results and summary to a report file.
        
        Arguments: 
        - report_path:str        (Path to output report file) 
        - task_ids:list[str],    (List of task IDs)
        - results:list[bool]     (Execution status for each task)

        Returns: None
    '''
    with open(report_path, 'w') as file:
        file.write("Task Feasibility Report\n\n")
        executable_count = 0
        non_executable_count = 0

        for i in range(len(task_ids)):
            task_id = task_ids[i]
            result = results[i]

            if result:
                file.write(f"{task_id}: executable\n")
                executable_count +=1
            else:
                file.write(f"{task_id}: not executable\n")
                non_executable_count +=1
            
        file.write("\n")
        file.write(f"Executable tasks: {executable_count}\n")
        file.write(f"Non-executable tasks: {non_executable_count}\n")

        
def main(robots_path: str, destination_path: str, packages_path: str,
         tasks_path: str, schedules_path: str, distances_path: str, 
         report_path: str, plot_file: str) -> None:

    robots = read_robots(robots_path)
    destination = read_destinations(destinations_path)
    packages = read_packages(packages_path)

    destination_ids = [d["destination_id"] for d in destinations]
    package_ids = [p["package_id"] for p in packages]

    tasks = read_tasks(tasks_path, destination_ids, package_ids)

    task_results = []
    for task in tasks:
        result = is_task_executable(task, robots, destinations, packages, tasks)
        task_results.append(result)

# -------------------------------------------------------------------------------------------------------
    robot_ids = [r["robot_id"] for r in robots]
    task_ids = [t["task_id"] for t in tasks]

    schedules = read_schedules(schedules_path, robot_ids, task_ids)
    distances = read_distances(distances_path)

    schedule_report = []
    for i in schedules:
        result = check_schedule(i, distances, robots, destinations, packages, tasks)
        schedule_report.append(result)

# -------------------------------------------------------------------------------------------------------
    
    task_ids = [t["task_id"] for t in tasks]

    write_feasibility_report(report_path, task_ids, task_results)

    with open(report_path, 'a') as file:
        
        file.write("\nSchedule Feasibility\n\n")

        for i in range(len(schedules)):
            schedule = schedules[i]
            result = schedule_report[i]

            if result is None:
                file.write(f"{schedule["schedule_id"]}: Infeasible\n")
            else:
                final = result[-1]
                file.write(f"{schedule["schedule_id"]}: Robot {schedule["robot_id"]} completed schedule in {final[0]:.2f} hours, covering {final[1]:.2f} km,battery remaining {final[3]:.2f}%.\n")

    plot_schedule_positions(schedules, schedule_report, plot_file)



    

    
