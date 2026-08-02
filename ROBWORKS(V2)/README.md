# 🤖 Robot Delivery Scheduling System

A Python-based delivery scheduling and logistics management system for autonomous delivery robots.

The project progressively evolves from loading and validating CSV data to building a complete delivery scheduling platform capable of validating robot tasks, simulating delivery schedules, generating feasibility reports, and visualising robot movement.

---

# 📋 Project Overview

This project simulates the backend software of an autonomous delivery company by providing tools to:

- Read and validate operational data
- Manage robot, package, destination, and task records
- Determine delivery feasibility
- Generate scheduling reports
- Simulate robot movement and battery consumption
- Visualise delivery schedules

The project is implemented across three increasingly complex stages.

---

# 🚀 Task 1 — Delivery Task Feasibility

Develop the core delivery scheduling engine.

## Features

### CSV Data Loading

Read operational data from multiple CSV files:

- robots.csv
- destinations.csv
- packages.csv
- tasks.csv

Each reader converts CSV data into aligned lists while preserving record consistency.

---

### Data Validation

Validate all incoming records before processing.

Validation includes:

#### Robots

- Battery level (0–100%)
- Maximum load
- Valid delivery zone

#### Destinations

- Valid delivery zone

#### Packages

- Non-negative package weight

#### Tasks

- Valid source destination
- Valid target destination
- Existing package
- Valid task status

Invalid records are skipped with descriptive warning messages.

---

### Task Feasibility

Determine whether a delivery task can be completed.

A task is considered executable when:

- A robot exists in the required delivery zone
- The robot can carry the package
- Required locations are valid

---

### Feasibility Report

Generate a report containing:

- Executable tasks
- Non-executable tasks
- Summary statistics

Example:

```
Task Feasibility Report

T1: executable
T2: executable
T3: not executable

Executable Tasks: 2
Non-executable Tasks: 1
```

---

# 🏗 Task 2 — Modular Delivery System

Refactor the system into reusable modules following good software engineering principles.

---

## Modular Architecture

Project divided into three independent modules.

```
reader.py
```

Responsible for:

- Reading CSV files
- Data validation
- Table creation

---

```
tasker.py
```

Responsible for:

- Delivery feasibility
- Scheduling logic
- Business rules

---

```
main.py
```

Responsible for:

- User interaction
- Report generation
- Program execution

---

## Data Tables

Replace aligned lists with structured data tables.

Each CSV is converted into:

```python
[
    {
        "robot_id": "R1",
        "battery_level": "85",
        ...
    }
]
```

This greatly improves readability and maintainability.

---

## Regex Validation

Uses Python's `re` module to validate:

- IDs
- Integers
- Floating-point values
- Delivery zones

All invalid records are automatically discarded.

---

## Improved Function Design

All business logic:

- avoids global variables
- receives data through parameters
- follows consistent argument ordering
- separates validation from presentation

---

# 🚚 Task 3 — Delivery Schedule Simulation

Extend the system to simulate complete robot delivery schedules.

---

## Schedule Loading

Read schedule information from:

```
schedules.csv
```

Each schedule contains:

- Schedule ID
- Robot ID
- Ordered list of delivery tasks

---

## Distance Matrix

Load destination distances from:

```
distances.csv
```

The distance matrix allows robots to calculate:

- travel distance
- travel time
- battery consumption

---

## Robot Simulation

The simulator models:

### Robot Movement

- Constant speed
- Direct travel between destinations

---

### Battery Consumption

Battery usage depends on:

- Travel distance
- Package weight
- Empty travel
- Loaded travel

---

### Schedule Validation

A schedule is feasible only if:

- Robot can carry every package
- Robot remains within battery limits
- All destinations belong to the robot's zone
- Robot returns safely to the origin

---

## Schedule Report

Generate a complete report including:

- Task feasibility
- Schedule feasibility
- Total travel distance
- Completion time
- Remaining battery

Example:

```
Schedule Feasibility

S1:
Robot R9 completed schedule
Time: 1.60 hours
Distance: 24.05 km
Battery Remaining: 11.01%

S2:
Infeasible
```

---

## Visualisation

Generate delivery schedule graphs using:

- Pandas
- Matplotlib

Each graph displays:

- Time (hours)
- Distance from origin (km)

Multiple robot schedules are plotted together for comparison.

---

# 📂 Project Structure

```text
.
├── reader.py
├── tasker.py
├── main.py
├── robots.csv
├── destinations.csv
├── packages.csv
├── tasks.csv
├── schedules.csv
├── distances.csv
├── feasibility_report.txt
├── schedule_plot.png
├── README.md
└── requirements.txt
```

---

# 🛠 Technologies

- Python 3
- CSV
- Regular Expressions (`re`)
- Pandas
- Matplotlib

---

# 📚 Programming Concepts Demonstrated

- File Processing
- CSV Parsing
- Data Validation
- Regular Expressions
- Modular Programming
- Separation of Responsibilities
- Dictionaries
- Lists
- Algorithm Design
- Inventory & Logistics
- Robot Scheduling
- Battery Simulation
- Data Visualisation

---

# 🔄 System Workflow

```
Read CSV Files
        │
        ▼
Validate Data
        │
        ▼
Create Data Tables
        │
        ▼
Check Task Feasibility
        │
        ▼
Generate Schedules
        │
        ▼
Simulate Robot Movement
        │
        ▼
Calculate Battery Usage
        │
        ▼
Generate Reports
        │
        ▼
Visualise Results
```

---

# 📈 Features Summary

- ✅ CSV Data Loading
- ✅ Input Validation
- ✅ Regex-Based Verification
- ✅ Task Feasibility Analysis
- ✅ Robot Schedule Validation
- ✅ Battery Consumption Simulation
- ✅ Delivery Time Estimation
- ✅ Report Generation
- ✅ Data Visualisation
- ✅ Modular Architecture

---

# 🎯 Learning Outcomes

This project demonstrates the development of a complete delivery scheduling system using Python, progressing from basic file processing to modular software engineering and logistics simulation.

Key learning outcomes include:

- Designing modular applications
- Reading and validating structured datasets
- Applying regular expressions for robust validation
- Building reusable business logic
- Simulating real-world delivery operations
- Managing robot constraints such as payload and battery life
- Producing analytical reports and visualisations
- Following clean software architecture principles

---

# 📄 License

This project was developed for educational purposes as part of a university programming assignment.
