import sys

# Write your functions here.
def read_robots(robots_path: str)-> tuple:
    '''
    Description : This function should take a path to a CSV file 
    containing information on the robots and return an aligned 
    list for each of the field contained in the CSV file, 
    in the order that they appear.

    Arguments : file_path(the actual path of CSV file).

    Return : ids and values of CSV file by extraction.
    '''
    robot_ids = []
    battery_levels = []
    max_loads = []
    robot_zones = []

    with open(robots_path, 'r') as file:
        next(file)
        for line in file:
            parts = line.strip().split(',')

            robot_id = parts[0]
            battery_level = parts[1]
            max_load = parts[2]
            zone = parts[3]

            # Safe conversation of the value: battery_level, and max_load
            battery_level = int(battery_level)
            max_load = float(max_load)

            # Validation: 
            if not (0 <= battery_level <= 100):
                print(f"Warning: Robot {robot_id} has invalid battery level ({battery_level})", file=sys.stderr)
                continue
            if max_load < 0:
                print(f"Warning: Robot {robot_id} has invalid max load ({max_load})", file=sys.stderr)
                continue
            if not (zone.isalpha() and zone.isupper()):
                print(f"Warning: Robot {robot_id} has invalid zone ({zone})", file=sys.stderr)
                continue
            
            # Appending valid records:
            robot_ids.append(robot_id)
            battery_levels.append(battery_level)
            max_loads.append(max_load)
            robot_zones.append(zone)

    return [robot_ids, battery_levels, max_loads, robot_zones]


def read_destinations(destinations_path: str) -> list[list]:
    '''
    Description: This function should take a CSV file containing information on the 
    destinations and return an aligned list for each of the fields contained in the 
    CSV file, in the order that they appear.

    Arguments : destinations_path: the path of destination information CSV file.

    Returns: destination ids and their zones. 
    '''
    destination_ids = []
    destination_zones = []

    with open(destinations_path, 'r') as file:
        next(file)

        for line in file:
            parts = line.strip().split(',')

            # Basic structure check:
            if len(parts)!=2:
                print("Warning: invalid destination record format", file=sys.stderr)
                continue
            
            destination_id = parts[0]
            zone = parts[1]

            # Validation
            if not (zone and zone.isalpha() and zone.isupper()):
                print("Warning: Destination {destination_id} has invalid zone ({zone})", file=sys.stderr)
                continue
            
            # Appending valid records:
            destination_ids.append(destination_id)
            destination_zones.append(zone)

    return [destination_ids, destination_zones]

def read_packages(packages_path: str)-> list[list]:
    '''
    Description: This function should take a CSV file containing information on the 
    packages and return an aligned list for each of the fields contained in the CSV 
    file, in the order that they appear.

    Arguments : (packages_path)the actual CSV file path that contains packages data.

    Returns: the list of package ids and corresponding weights
    '''

    package_ids = []
    weights = []

    with open(packages_path, 'r') as file:
        next(file)

        for line in file:
            parts = line.strip().split(',')

            # Basic Structure check:
            if len(parts) != 2:
                print("Warning: invalid package record format", file=sys.stderr)
                continue
            
            package_id = parts[0]
            weight = parts[1]

            # Safely convert:
            weight = float(weight)

            # Validation
            if weight < 0:
                print(f"Warning: Package {package_id} has invalid weight ({weight})", file=sys.stderr)
                continue

            # Appending valid data
            package_ids.append(package_id)
            weights.append(weight)

    return [package_ids, weights]

def read_tasks(tasks_path: str, destination_ids: list[str] , package_ids: list[str]) -> list[list]:
    '''
        Description: This function should take a CSV file containing information on the tasks 
        and return an aligned list for each of the fields contained in the CSV file, in the 
        order that they appear.

        Arguments: task_path(file path of tasks)
                   destiny_ids(Ids of destination)
                   package_ids(Ids of packages)
        Returns: All values of : 
                    task_ids
                    source_ids
                    target_ids
                    task_package_ids
                    statuses
    '''

    task_ids = []
    source_ids = []
    target_ids = []
    task_package_ids = []
    statuses = []

    with open(tasks_path, 'r') as file:
        next(file)

        for line in file:
            parts = line.strip().split(',')

            # Basic structure check:
            if len(parts)!= 5:
                print(f'Warning: invalid task record format', file=sys.stderr)
                continue

            task_id = parts[0]
            source_id = parts[1]
            target_id = parts[2]
            package_id = parts[3]
            status = parts[4]

            # Validation
            if source_id not in destination_ids:
                print(f'Warning: Task {task_id} has invalid source ({source_id})',file=sys.stderr)
                continue

            if target_id not in destination_ids:
                print(f'Warning: Task {task_id} has invalid target ({target_id})', file=sys.stderr)
                continue

            if package_id not in package_ids:
                print(f'Warning: Task {task_id} has invalid package ({package_id})', file=sys.stderr)
                continue

            if status not in ['pending', 'complete']:
                print(f'Warning: Task {task_id} has invalid status ({status})', file=sys.stderr)
                continue

            # Appending all valid information:
            task_ids.append(task_id)
            source_ids.append(source_id)
            target_ids.append(target_id)
            task_package_ids.append(package_id)
            statuses.append(status)

    return [task_ids, source_ids, target_ids, task_package_ids, statuses]
            
def is_task_executable(task_id:str, package_ids:list[str], 
    package_weights:list[float], robot_ids:list[str], 
    max_loads:list[float], robot_zones: list[str], 
    destination_ids:list[str], destination_zones:list[str], 
    task_ids: list[str], source_ids:list[str], 
    target_ids:list[str], task_package_ids:list[str]) -> bool:

    '''
        Description: Determines if a task can be executed by any available robot.
        Arguments: 
            - task_id:str                    (ID of the task to evaluate)
            - package_ids:list[str],         (List of all package IDs)
            - package_weights:list[float],   (Corresponding package weights)
            - robot_ids:list[str],           (List of robot IDs)
            - max_loads:list[float],         (Max load capicity of each robot)
            - robot_zones: list[str],        (Zone assigned to each robot)
            - destination_ids:list[str],     (List of destination IDs)
            - destination_zones:list[str],   (Corresponding zones for destinations)
            - task_ids: list[str],           (List of task IDs)
            - source_ids:list[str],          (Source destination IDs per task)
            - target_ids:list[str],          (Target destination IDs per task)
            - task_package_ids:list[str]     (Package IDs assigned to each task)

        Returns: True if task is executable, otherwise False
    '''
    # Find the task index:
    task_index = task_ids.index(task_id)

    # Get package_id and weight:
    package_id = task_package_ids[task_index]
    package_index = package_ids.index(package_id)
    package_weight = package_weights[package_index]

    # Get source and target zones:
    source_id = source_ids[task_index]
    target_id = target_ids[task_index]

    source_index = destination_ids.index(source_id)
    target_index = destination_ids.index(target_id)

    source_zone = destination_zones[source_index]
    target_zone = destination_zones[target_index]

    # check robots :
    for i in range(len(robot_ids)):
        if robot_zones[i] == source_zone and robot_zones[i] == target_zone:
            if max_loads[i] >= package_weight:
                return True
            
    return False

def write_feasibility_report(report_path:str, task_ids:list[str], results:list[bool]) -> None:
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
    robot_data = read_robots(robots_path)
    destination_data = read_destinations(destinations_path)
    package_data = read_packages(packages_path)
    task_data = read_tasks(tasks_path, destination_data[0], package_data[0])

    # Data unpacking:
    robot_ids, battery_levels, max_loads, robot_zones = robot_data
    destination_ids, destination_zones = destination_data
    package_ids, package_weights = package_data
    task_ids, source_ids, target_ids, task_package_ids, statuses = task_data

    # Task evaluation:
    results = []

    for task_id in task_ids:
        result = is_task_executable(task_id, package_ids, package_weights, robot_ids, max_loads, robot_zones, destination_ids, destination_zones, task_ids, source_ids, target_ids, task_package_ids)
        results.append(result)
    
    # Report writing:
    write_feasibility_report(report_path, task_ids, results)

if __name__ == "__main__":
    # Write your test code here.

    print("This is an example of how you should write to the standard error buffer, stderr.")

