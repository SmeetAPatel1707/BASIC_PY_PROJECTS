Task 1: One task at a time
RoboWorks operates a fleet of delivery robots, and your team has been asked to develop a delivery scheduling system. Since this is a complex system, you will build it step by step.

Step 1: Implement the data loading component.
You are provided with four CSV files:

robots.csv

destinations.csv

packages.csv

tasks.csv

Sample CSV files can be found in the section labelled Sample CSV File. We will continue to update this slide with sample data.

You must implement the following functions:

read_robots(...) - This function should take a path to a CSV file containing information on the robots and return an aligned list for each of the field contained in the CSV file, in the order that they appear.

read_destinations(...) - This function should take a CSV file containing information on the destinations and return an aligned list for each of the fields contained in the CSV file, in the order that they appear.

read_packages(...) - This function should take a CSV file containing information on the packages and return an aligned list for each of the fields contained in the CSV file, in the order that they appear.

read_tasks(...) - This function should take a CSV file containing information on the tasks and return an aligned list for each of the fields contained in the CSV file, in the order that they appear. This function should take additional ID data as lists of IDs, required in step 2.

For the file path you should use the name followed by term path. For example read_robots should take the parameter robots_path 

Each function should:

Read data from the corresponding CSV file

Store the data using aligned lists in a type that is consistent with the data being stored.

Ensure that corresponding indices refer to the same record

Step 2: Perform basic validation.
You should perform basic validation while reading the data. Records with invalid values should be skipped and a warning message should be printed. IDs do not need to validated as part of this task.

For task 1, you should assume that all data types are correct in the input files. The bounds of the data is not guaranteed.

For robots.csv and similar files:

battery_level must be an integer between 0 and 100.

max_load must be a non-negative floating point number.

zone must be a non-empty string consisting of only upper case alphabetical characters.

For destinations.csv and similar files:

zone must be a non-empty string consisting of only upper case alphabetical characters.

For packages.csv and similar files:

weight must be a non-negative floating point number.

For tasks.csv and similar files:

source_id must exist in the destination data,

target_id must exist in the destination data,

package_id must exist in the package data,

status must be one of pending or complete.

If a record is invalid, it should be skipped and a warning message should be printed to the standard error buffer (See Appendix A on printing to non-standard buffers).

Example:

Warning: Package P6 has invalid weight (-4).

Warning messages should be customised to the record being validated. The specific structure of the warning message is up to you. The warning message must be indicative of the issue detected.

Step 3: Perform task feasibility checking.
After loading and validating the data, you will need to determine whether each task is executable. A task is considered executable if there exists at least one robot that:

is in the same zone as both the source and the target,

the robot has sufficient load capacity for the package.

At this stage, you do not need to consider robot availability or battery constraints.

To determine if a task is executable, create a function named is_task_executable. This task should take the following parameters, in this order:

task_id

package_ids

package_weights

robot_ids

max_loads

robot_zones

destination_ids

destination_zones

task_ids

source_ids

target_ids

task_package_ids

You should infer the types of the input variables from the name of the parameters.

Step 4: Forming a feasibility report.
Your program should be able to write a feasibility report to a file named feasibility_report.txt. To do this, your program should contain the function write_feasability_report. This function should take as input, a file path, a list of task IDs and a corresponding list of results containing a bool to indicate whether or not the task is feasible.

As example report is given below:

Task Feasibility Report

T1: executable
T2: executable
T3: not executable
T4: executable

Executable tasks: 3
Non-executable tasks: 1

Completion of the program.
Finally your program should contain the a main function that takes as input parameters the file paths, in the order that they appear in step 1, and writes a feasibility report to a file_path that is specified as the last parameter.

main(robots_path, destinations_path, packages_path, tasks_path, report_path)

A main guard has been provided, all other code you wish to add as testing code should be contained in the main guard.

You may not use any imports that have not been included in the scaffold file or explicitly mentioned in this task.


//////////////////////////////////////////////////////////////////////////////////////

Task 2: Modular validation
The initial delivery scheduling system is working well but has some serious limitations with respect to usability and design. In this task, you will correct this oversight.

Step 1: Separation of responsibility.
Using your file main.py from task 1 as a basis, you should create 3 files, reader.py, tasker.py, and main.py. These files should have the following responsibilities:

reader.py: This file should contain all the functions and logic used to read and validate the CSV files.

tasker.py: This file should contain all the functions and logic required to carry out task related activities after the files have been read.

main.py: This file should contain all the functions and logic required for printing to the console and writing files, based off the given CSV files.

Note: Printing to stderr does not count as output and can happen at any time from any function.

Step 2: Organising your data.
To improve our program further, we want to create a sensible collection of records for each CSV file. To do this, we will no longer rely on aligned lists and will instead think in terms of data tables. A data table is a list of dictionaries. The elements of the list represent the rows of the table. The rows themselves are dictionaries that map the header of the CSV file to the data contained. This process is generic across all the files that we have given you. As such you are required to write a function read_to_table(...) that takes a path to a CSV file as input and returns the appropriate data table. This function should be entirely general and should be able to handle any CSV with header values. As the type information is not generic across all CSVs, all the values in your dictionary should be stored as strings in the return value of this function.

You must update all functions that read CSV files to use the read_to_table function. Additionally all existing functions should be updated to use the new data tables, both as output and as input parameters.

Functions that require additional data, such as read_tasks requiring a list of destination IDs, should not have the type of this data changed. In other words, functions required for validation should still take lists of valid ID's not a data table.

Step 3: Validation using the RE library.
The following step requires the use of the regular expression module for the python standard library. Please see the regular expression appendix.

All input files must be validated. To do this, you will use the regular expression library (re) to validate all CSV data that requires validation. This includes, but is not limited to, integers, floats, IDs, and zones.

Each line of data will have a unique ID. These IDs are not shared across different types of data. This is a guarantee of the input data and does not need to be checked. Each ID follows a particular form, the ID consists of one or more upper case alphabetical character followed by a sequence of digits representing a non-negative integer. For example, AB123 is a valid ID, however, AB0456 is not. For this task, you need to check the form of an ID.

This validation should be in addition to the existing bounds checking. If a row is invalid, you should print a warning and discard the row, as in task 1.

The regular expression library uses the meta-programming language known as regex for pattern matching. To use this appropriately, you must understand what strings represent certain types in python. The string formats for IDs and zones are given in the previous task. In addition to these formats we can map from python types to string formats in the following way:

int: We will consider an integer to be represented by a string of digits that may or may not be preceded by a minus sign. The integer 0 is the only integer with a leading digit of 0. The integer 0 may be represented by either 0 or -0. Examples of valid integer representations: 1, 345, -345. Examples of invalid integer representations: 01, 10-, 000, --3.

float: A python float is represented by a string of digits followed by a decimal point followed by another string of digits. The only floats that have a leading 0 are the floats in the range 
−
1
<
i
<
1
−1<i<1. Floats may be preceded by a minus sign, -. The only floats ending in a 0 after the decimal point are whole numbers, which end with exactly one 0. All int representations are also valid float representations.

Step 4: Wrapping it all together
As a final step, you must ensure that the new program has the full capabilities of the old program. However, should be modified to include the new data tables. The following conventions should be followed:

All functions should use tables rather than aligned lists, wherever possible.

All data obtained from CSV files must be passed as arguments to functions and must not be used in any global namespace.

All function arguments should be named appropriately, singular names should be used for rows; a single task record should use an argument named task, for example. A table of destinations should use an argument named destinations.

Finally, when updating your functions, all arguments should have the the following order in the function signature:

robot

desintation

package

task

robots

destinations

packages

tasks

Hint: when thinking about is_task_executable you require access to the given task, the robots, the destinations, and the packages (in that order). In this example, we only include the arguments required.

//////////////////////////////////////////////////////////////////////////////////////

Task 3: Schedule this!
The following task seeks to round out the notion of a delivery system. Initialise your directory by making copies of your files from task 2. Remember that you should maintain the same separation of responsibilities that you implemented for task 2.

Step 1: Addition of schedules.
To complete the system, you are required to implement logic to determine if the robots can complete a list of schedules. A schedule is simply a list of tasks assigned to a robot. You do not have to produce the schedules, these will be provided for you. A list of sample schedules has been provided in the file schedules.csv, sample files can be found here. These schedule files contain a schedule ID, a robot ID, and then one or more task IDs. Each task will be completed by the robot in order until there are no more tasks, or the robot is unable to continue.

As a first step, write a function read_schedules which takes as input a path to a schedule file, a list of valid robot IDs, and a list of valid task IDs. The function should read the rows of the schedule file, one line at a time, and return a list of dictionaries, where the dictionary contains the schedule ID (key schedule_id), robot ID (key robot_id), and a list of task IDs (key task_ids).

Note: You will not be able to use your generic CSV reading function as this file does not have a header.

The result of reading the schedules file should be validated, as in task 1 and 2.

Step 2: O destination, where art thou?
Before you can determine the success or failure of any given schedule, you need to know the relative locations of the destinations. Luckily, you will be provided with the distance information. The sample file distances.csv contains the relative distances of the destinations as an adjacency matrix (fancy term for a big grid). The first row and column of this matrix indicate the home base, where the robots start from and must return to. The remaining rows and columns then reference the destinations as provided in the destinations.csv, sample files can be found here. For simplicity, a distances file will only be provided when the destinations file has no error and therefore no skipped rows.

Consider the following example of possible distance and destination files:

destination_id,zone
D1,B
D2,B
D3,C
D4,A

0.00,4.51,8.74,8.18,8.17
4.51,0.00,6.46,10.13,5.99
8.74,6.46,0.00,7.98,0.56
8.18,10.13,7.98,0.00,7.68
8.17,5.99,0.56,7.68,0.00

From the table we see that the relative distance of D2 to D3, at row index 2 and column index 3, is 7.98 km (highlighted in bold), as an example. With the distance from the origin to D2 , at row index 0 and column index 2, being 8.74 km (highlighted in bold).

Note: The matrix is necessarily symmetric and can be read from either direction.

You must write a function called read_distances which takes as input a path to a file and returns a list of lists containing the distances in the format specified above. This function does not require any data validation.

Tip: When using this list of lists, remember that the destination contained in position i of the destinations corresponds to position i+1 in the distances matrix. This is because the i = 0 index is reserved for the origin.

Step 3: Satisfying a schedule.
We now need to extend the feasibility report to include schedule data. To do this we need to understand how the robots collect and deliver packages.

Robot movement - To keep things simple we assume instantaneous speed. So robots do not need to speed up, or slow down. Robot move at a uniform speed of 15 km per hour and always take a direct route to the destination.

Battery life - Robot batteries drain at a rate of 1% per km when not carrying a package. When carrying a package, a robot battery drains an additional 0.5% per kilogram per kilometer. So a robot carrying a 2 kg package 3 km will lose 6% of the robots battery.

Pick up and drop off - Robots can both pickup a package drop off a package instantly, regardless of weight. To pickup a package, a robot must first fly to the source destination and must fly to the target to drop the package off.

A schedule is feasible if it meets the following conditions:

The robot is able to carry every package in the schedule.

The robot is able to return to the origin without reaching 0.0% battery (except possibly at the origin).

All destinations in the schedule are in the same zone as the robot.

The robot does not return to the origin until they have complete every task.

Write a function called check_schedule that takes as input a schedule and a distance matrix followed by any other required data tables (remember the ordering of parameters). If the schedule is feasible, the function should then return a list of tuples where each tuple marks the state of the robot after travelling, except for the first tuple which is the initial state of the robot. The elements of the tuple should be:

The time elapsed, in hours.

The distance travelled, in km.

The distance of the robot from the origin, in km.

And finally the battery level, as a percentage.

If the schedule is not feasible, the function should return None. You should then update your feasibility report, extending it to contain the schedule information. The function should contain two new parameters called schedules, which contains the list of schedule rows, and the schedule_report, which contains a list containing the result of check_schedule for each schedule.

An example of the output of write_feasibility_report is given below:

Task Feasibility Report

T1: executable
T2: executable
T3: executable
T4: executable
T5: executable
T6: executable
T7: executable
T8: executable
T9: executable
T10: executable
T11: executable
T12: executable
T13: executable
T14: executable
T15: executable

Executable tasks: 15
Non-executable tasks: 0

Schedule feasibility

S1: Robot R9 completed schedule in 1.60 hours and covered 24.05 km. Battery remaining 11.01%.
S2: Infeasible
S3: Infeasible
S4: Robot R1 completed schedule in 1.10 hours and covered 16.45 km. Battery remaining 19.86%.
S5: Robot R10 completed schedule in 2.40 hours and covered 36.04 km. Battery remaining 21.15%.

Step 4: Visualisation
For each feasible schedule, plot the robot’s distance from the origin over time.

The x-axis should represent time (in hours).

The y-axis should represent the distance from the origin (in km).

You should use:

pandas to organise the output of check_schedule.

matplotlib to generate the plot.

All feasible schedules should be plotted on the same figure, with each schedule shown as a separate line with the robot labelled appropriately.

Your program should save the plot to a file, given by a parameter plot_file.

You should implement a function called plot_schedule_positions.

This function should take as input:

schedules: A list of schedule dictionaries, as returned by read_schedules.

schedule_report: A list containing the result of check_schedule for each schedule.

plot_file: The name of the file to write the plot to.

Remember, each element of schedule_report will either be:

None, if the schedule is infeasible,

or a list of tuples describing the robot’s state over time.

The function should generate a plot showing the robot’s distance from the origin over time for each feasible schedule, and save the plot to a file.

There is no strict required format for the plot. You may choose any clear and readable visualisation.

A possible example of the visualisation is shown below.
https://static.au.edusercontent.com/files/O4JJwwTvAkO7dLyQcKyf3srL
