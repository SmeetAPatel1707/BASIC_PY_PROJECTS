import traceback as tb

def check_schedule(schedule: dict, distances: list[list[float]], robots: list[dict], destinations: list[dict], packages: list[dict], tasks: list[dict]) -> list[tuple]:
    '''
        Description: This function takes as input a schedule and a distance matrix followed by any other required data tables.

        Arguments: 
        - schedule:
        - distances: 
        - robots:
        - destinations:
        - packages:
        - tasks:

        Returns: 
        - list of state tuples
    '''
    try:

        robot = next((r for r in robots if r["robot_id"] == schedule["robot_id"]), None)
        if robot is None:
            return None

        robot_zone = robot["zone"]
        battery = robot["battery_level"]
        max_load = robot["max_load"]

        destination_index = {d["destination_id"]: i+1 for i, d in enumerate(destinations)}
        package_map = {p["package_id"]: p["weight"] for p in packages}
        task_map = {t["task_id"]: t for t in tasks}

        time = 0.0
        total_distance = 0.0
        current_position = 0

        states = [(time, total_distance, 0.0, battery)]

        for task_id in schedule["task_ids"]:
            task = task_map[task_id]

            if task["status"] == "complete":
                continue

            source = task["source_id"]
            target = task["target_id"]
            package_id = task["package_id"]

            source_zone = next((d["zone"] for d in destinations if d["destination_id"]== source), None)
            target_zone = next((d["zone"] for d in destinations if d["destination_id"]== target), None)

            if source_zone != robot_zone or target_zone != robot_zone:
                return None
            
            weight = package_map[package_id]

            if weight > max_load:
                return None

            # By moving to the source.

            source_index = destination_index[source]
            dist = distances[current_position][source_index]

            battery = battery - (dist * 1)
            if battery <= 0:
                return None

            time = time + (dist/15)
            total_distance = total_distance + dist
            current_position = source_index

            distance_from_origin = distances[0][current_position]

            states.append((time, total_distance, distance_from_origin, battery))

            # By moving to target value.
            target_index = destination_index[target]
            dist = distances[current_position][target_index]

            battery = battery - (dist * (1 + (0.5 * weight)))
            if battery <= 0:
                return None

            time = time + (dist/15)
            total_distance = total_distance + dist
            current_position = target_index

            distance_from_origin = distances[0][current_position]

            states.append((time, total_distance, distance_from_origin, battery))

        # By returning to origin.
        dist = distances[current_position][0]
        battery = battery - (dist * 1)
        if battery <= 0:
            return None

        time = time + (dist/15)
        total_distance = total_distance + dist
        current_position = 0
        states.append((time, total_distance, 0.0, battery))

        return states

    except Exception as e:
        print(f"REAL ERROR...")
        tb.print_exc()
        raise

def is_task_executable(
    task: dict,
    robots: list[dict],
    destinations: list[dict],
    packages: list[dict],
    tasks: list[dict]
) -> bool:

    '''
        Description: Determines if a task can be executed by any available robot.

        Arguments: 
        - task (dict): A single task record
        - robots (list[dict]) : List of robot records
        - Destinations (list[dict]): list of destination records
        - packages (list[dict]): List of package records
        - tasks : List of all task records

        Returns: 
        - bool: True if executable, else False
    '''

    # Get package weight
    package_id = task["package_id"]
    package_weight = None

    for pkg in packages:
        if pkg["package_id"] == package_id:
            package_weight = pkg["weight"]
            break
        
    if package_weight is None:
        return False

    # Get source and target zones :
    source_id = task["source_id"]
    target_id = task["target_id"]

    source_zone = None
    target_zone = None

    for dest in destinations:
        if dest['destination_id'] == source_id:
            source_zone = dest["zone"]
        if dest["destination_id"] == target_id:
            target_zone = dest["zone"]

    if source_zone is None or target_zone is None:
        return False

    # Checking robots

    for robot in robots:
        if robot['zone'] == source_zone and robot["zone"] == target_zone:
            if robot['max_load'] >= package_weight:
                return True
        if source_zone != target_zone:
            return False

    return False
