# 🤖 Robot Manufacturing System

A Python-based inventory and order management system developed for a fictional robotics manufacturing company.

The project is divided into three progressively advanced tasks that demonstrate fundamental programming concepts including data structures, functions, inventory management, order processing, and API design.

---

# 📋 Project Overview

This project simulates the workflow of a robotics manufacturing company by providing tools to:

- Calculate customer quotations
- Manage inventory
- Process production orders
- Handle backorders
- Calculate discounts
- Expose reusable API functions
- Provide an interactive Command-Line Interface (CLI)

---

# 🚀 Task 1 — Quote Calculator

Develop a quotation system for a simple electronics division.

## Features

- Store products using aligned lists
- Request customer quantities for each product
- Calculate individual line totals
- Calculate subtotal
- Apply business discount rules
- Display final quotation

### Products

| Product | Price |
|----------|-------:|
| Motor | $49.99 |
| Sensor | $15.75 |
| Frame | $120.00 |
| CPU | $85.50 |

### Quote Output

The calculator displays:

- Product quantity
- Unit price
- Line total
- Subtotal
- Discount
- Final total

---

# 📦 Task 2 — Order Queue Processor

Simulates a manufacturing system that processes robot orders while tracking inventory.

## Features

### Inventory Management

Maintain current stock for all robot components using aligned lists.

Tracked components include:

- Servo
- Lidar
- Motor
- Sensor
- Gyroscope
- Gearbox
- Regulator
- Controller

---

### Robot Models

Supports four robot models:

- R1
- R2
- R3
- R4

Each model stores its required components using a dictionary of aligned lists.

Example structure:

```python
models = {
    "R1": [...],
    "R2": [...],
    "R3": [...],
    "R4": [...]
}
```

---

### Order Queue

Orders are processed sequentially.

Example:

```python
[
    ("R4", 2),
    ("R1", 2),
    ("R3", 1),
    ("R2", 4)
]
```

---

### Order Processing

For every order, the system:

1. Checks inventory availability
2. Determines build feasibility
3. Updates inventory
4. Calculates revenue
5. Tracks successful builds
6. Places unbuildable units on backorder

---

### Production Report

After processing all orders, the system generates:

- Constructed robots per model
- Total production revenue
- Backordered units
- Remaining inventory

---

# ⚙️ Task 3 — Mini API with CLI

Extends the manufacturing system into a reusable API with an interactive command-line interface.

---

## API Functions

### `get_model_cost()`

Calculates the manufacturing cost of a robot model.

---

### `can_build_one()`

Determines whether sufficient inventory exists to construct a robot.

Returns:

- `True`
- `False`

---

### `build_one()`

Builds a single robot by:

- validating inventory
- deducting required components
- returning production cost

Returns:

- Robot cost
- `$0.00` if construction is impossible

---

### `process_order()`

Processes an entire customer order.

Returns:

```python
(
    units_built,
    units_on_backorder,
    total_cost
)
```

---

### `apply_discount()`

Applies the company's pricing discount policy to an order total.

---

# 💻 Command Line Interface

Interactive menu-driven application.

```
1) Show models and costs
2) Attempt order
3) Show inventory
0) Exit
```

Supported operations include:

- View available robot models
- Display manufacturing costs
- Place production orders
- Check inventory
- Exit application

---

# 🏗 Project Structure

```text
.
├── task1.py
├── task2.py
├── task3.py
├── README.md
└── requirements.txt
```

---

# 🛠 Technologies

- Python 3
- Standard Library only

Concepts used:

- Lists
- Dictionaries
- Tuples
- Functions
- Loops
- Conditionals
- Input Validation
- Inventory Management
- Command-Line Interface (CLI)

---

# 📚 Programming Concepts Demonstrated

- Data Structures
- Modular Programming
- Separation of Responsibilities
- Function Design
- Inventory Tracking
- Order Processing
- Business Logic
- API Design
- User Interaction
- Input Validation

---

# 🧪 Example Workflow

```
Start Program
      │
      ▼
Display Menu
      │
      ▼
Select Action
      │
      ├── View Robot Costs
      ├── Place Order
      ├── View Inventory
      └── Exit
      │
      ▼
Process Request
      │
      ▼
Display Result
```

---

# 🎯 Learning Outcomes

This project demonstrates how to design a small-scale manufacturing management system using core Python programming principles.

Key skills include:

- Building reusable APIs
- Designing modular software
- Managing inventory efficiently
- Processing customer orders
- Applying business rules
- Separating business logic from user interfaces
- Developing maintainable command-line applications

---

# 📄 License

This project was developed for educational purposes as part of a university programming assignment.
