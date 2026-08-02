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

    return False
