from reader import read_robots, read_destinations, read_packages, read_tasks
from tasker import is_task_executable

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


def main(robots_path:str, destinations_path:str, packages_path:str, tasks_path:str, report_path:str) -> None:
    '''
    Description: Coordinates data loading, task evaluation, and report generation.

    Arguments: 
    - robots_path:str          (Path to robots CSV file) 
    - destinations_path:str,   (Path to destinations CSV file)
    - packages_path:str,       (Path to packages CSV file)
    - tasks_path:str,          (Path to tasks CSV file)
    - report_path:str          (Path to output feasibility report file)
    
    Returns: None
    '''

    # Loading data...
    robots = read_robots(robots_path)
    destinations = read_destinations(destinations_path)
    packages = read_packages(packages_path)

    destination_ids = [d["destination_id"] for d in destinations]
    package_ids = [p["package_id"] for p in packages]

    tasks = read_tasks(tasks_path, destination_ids, package_ids)


    # Task evaluation:
    results = []

    for task in tasks:
        result = is_task_executable(task, robots, destinations, packages, tasks)
        results.append(result)

    task_ids = [t["task_id"] for t in tasks]
    
    # Report writing:
    write_feasibility_report(report_path, task_ids, results)
