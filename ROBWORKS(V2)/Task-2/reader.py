import re
import sys

def read_to_table(path:str) -> list[dict]:
    '''
    Description : Reads a CSV file and returns data as a list of dictionaries.

    Arguments: file_path(str): Path to CSV file

    Returns : list: table representation of CSV with string values.
    '''
    table = []
    with open(path, 'r') as file:
        header = file.readline().strip().split(',')

        for line in file:
            values = line.strip().split(',')

            if len(values) != len(header):
                print("Warning: invalid row format")
                continue
            
            row = {}
            for i in range(len(header)):
                row[header[i]] = values[i]

            table.append(row)
    return table


# Validation Helper functions: 
def is_valid_id(value:str) -> bool:
    return bool(re.match(r'^[A-Z]+[1-9][0-9]*$', value))

def is_valid_int(value:str) -> bool:
    return bool(re.match(r'^-?(0|[1-9][0-9]*)$', value))

def is_valid_float(value:str) -> bool:
    # check valid integer
    if re.fullmatch(r'-?(0|[1-9][0-9]*)', value):
        return True

    if re.fullmatch(r'-?(0|[1-9][0-9]*)\.[0-9]+', value):

        decimal_part = value.split('.')[1]
        # integer_part, decimal_part = value.split('.')

        # reject trailing zeros except single 0
        if decimal_part.endswith('0') and decimal_part != '0':
            return False

        return True

    return False

def is_valid_zone(value:str) -> bool:
    return bool(re.match(r'^[A-Z]+$', value))


def read_robots(robots_path:str) -> list[dict]:
    '''
        Description: Reads robots CSV, validates records, and returns valid robot table.

        Arguments : 
        - robots_path: Path to robots CSV file

        Returns: 
        -list[dict]: Valid robot records as table
    '''

    raw_table = read_to_table(robots_path)
    robots = []

    for robot in raw_table:
        robot_id = robot["robot_id"]
        battery = robot["battery_level"]
        max_load = robot["max_load"]
        zone = robot["zone"]

        if not is_valid_id(robot_id):
            print(f"Warning: Robot {robot_id} has invalid ID",file=sys.stderr)
            continue

        if not is_valid_int(battery):
            print(f"Warning: Robot {robot_id} has invalid battery format)", file=sys.stderr)
            continue
        
        battery_val = int(battery)
        if not (0 <= battery_val <= 100):
            print(f"Warning: Robot {robot_id} has invalid batter level ({battery})", file=sys.stderr)
            continue

        if not is_valid_float(max_load):
            print(f"Warning: Robot {robot_id} has invalid max load format", file=sys.stderr)
            continue
        
        if float(max_load) < 0:
            print(f"Warning: Robot {robot_id} has invalid max load ({max_load})", file=sys.stderr)
            continue
        
        if not is_valid_zone(zone):
            print(f"Warning: Robot {robot_id} has invalid zone ({zone})", file=sys.stderr)

        validated_robot = {
            "robot_id": robot_id,
            "battery_level": battery_val,
            "max_load": float(max_load),
            "zone": zone
        }

        robots.append(validated_robot)

    return robots


def read_destinations(destinations_path:str) -> list[dict]:
    '''
    Description: Reads destination CSV, validates records, and returns valid destination table.

    Arguments: 
    - destination_path : Path to destination CSV file

    Returns: 
    - list[dict]: Valid destination records as table
    '''

    raw_table = read_to_table(destinations_path)
    destinations = []

    for dest in raw_table:
        dest_id = dest["destination_id"]
        zone = dest["zone"]

        if not is_valid_id(dest_id):
            print(f"Warning: Destination {dest_id} has invalid ID", file=sys.stderr)
            continue
        
        if not is_valid_zone(zone):
            print(f"Warning: Destination {dest_id} has invalid zone ({zone})", file=sys.stderr)
            continue
        
        destinations.append(dest)
    return destinations

def read_packages(packages_path:str) -> list[dict]:
    '''
    Description: Reads packages CSV, validates records, and returns valid package table.

    Arguments: 
    - packages_path : Path to packages CSV file

    Returns: 
    - list[dict]: Valid package records as table
    '''
    raw_table = read_to_table(packages_path)
    packages = []

    for pkg in raw_table:
        package_id = pkg["package_id"]
        weight = pkg["weight"]

        if not is_valid_id(package_id):
            print(f"Warning: Package {package_id} has invalid ID", file=sys.stderr)
            continue
        
        if not is_valid_float(weight):
            print(f"Warning: Package {package_id} has invalid weight format", file=sys.stderr)
            continue

        if float(weight) < 0:
            print(f"Warning: Package {package_id} has invalid weight ({weight})", file=sys.stderr)
            continue

        validated_package = {
            "package_id": package_id,
            "weight": float(weight)
        }
        
        packages.append(validated_package)

    return packages

def read_tasks(tasks_path: str, destination_ids:list[str], package_ids:list[str]) -> list[dict]:
    '''
    Description: Reads tasks CSV, validates records, and returns valid task table

    Arguments: 
    - tasks_path : Path to tasks CSV file
    - destination_ids : Valid destination IDs
    - package_ids : Valid package IDs

    Returns: 
    - list[dict]: Valid task records as table
    '''

    raw_table = read_to_table(tasks_path)
    tasks = []

    for task in raw_table:
        task_id = task["task_id"]
        source = task["source_id"]
        target = task["target_id"]
        package = task["package_id"]
        status = task["status"]

        if not is_valid_id(task_id):
            print(f"Warning: Task {task_id} has invalid ID", file=sys.stderr)
            continue
        
        if source not in destination_ids:
            print(f"Warning: Task {task_id} has invalid source ({source})", file=sys.stderr)
            continue

        if target not in destination_ids:
            print(f"Warning: Task {task_id} has invalid target ({target})", file=sys.stderr)
            continue

        if package not in package_ids:
            print(f"Warning: Task {task_id} has invalid package ({package})", file=sys.stderr)
            continue

        if status not in ['pending', 'complete']:
            print(f"Warning: Task {task_id} has invalid status ({status})", file=sys.stderr)
            continue

        tasks.append(task)

    return tasks
