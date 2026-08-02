Task 1 - Quote Calculator (Assessed)
Your boss now wants you to take what you have learned a create a functional quote calculator for the simple electronics division. Your boss would like you to formalise what you did in subtask 1.2 by creating two aligned lists product_name, containing a list of product names, and product_price, containing a list of product prices. You should populate this list using the table below.

-----------------------
Product Name | Price
-----------------------
motor        |  $49.99
sensor       |  $15.75 
frame        | $120.00
cpu          |  $85.50

You must conform to the variable naming given in the task. In testing, we will manipulate these lists. If they are not named correctly, then you will fail the tests and lose the marks.

Your program will then prompt the user for a desired quantity of each part from the list product_name. Using this information you will compute the line total for each item, the subtotal for all items, the discount (in dollars, even if $0.00), and the total price.

Examples:

Welcome to the RoboWorks Quote Calculator.

For each product below, please specify your required quantity.

motor: 1
sensor: 2
frame: 3
cpu: 4

Please see your quote below.

motor: 1 x $49.99 = $49.99
sensor: 2 x $15.75 = $31.50
frame: 3 x $120.00 = $360.00
cpu: 4 x $85.50 = $342.00

Subtotal: $783.49
Discount: $39.17
Total: $744.32

Welcome to the RoboWorks Quote Calculator.

For each product below, please specify your required quantity.

motor: 2
sensor: 1
frame: 0
cpu: 0

Please see your quote below.

motor: 2 x $49.99 = $99.98
sensor: 1 x $15.75 = $15.75
frame: 0 x $120.00 = $0.00
cpu: 0 x $85.50 = $0.00

Subtotal: $115.73
Discount: $0.00
Total: $115.73

Welcome to the RoboWorks Quote Calculator.

For each product below, please specify your required quantity.

motor: 5
sensor: 6
frame: 15
cpu: 8

Please see your quote below.

motor: 5 x $49.99 = $249.95
sensor: 6 x $15.75 = $94.50
frame: 15 x $120.00 = $1800.00
cpu: 8 x $85.50 = $684.00

Subtotal: $2828.45
Discount: $424.27
Total: $2404.18


/////////////////////////////////////////////////////////////////////////////////////////////////////

Task 2 - Order Queue Processor (Assessed)
Your boss looks over the programs you have written and decides that you are ready to write the Order Queue Processor.

As part of this program, you are given an updated stock table. 

| Part Name   |   Part Stock | Part Cost   |
|-------------|--------------|-------------|
| servo       |           42 | $38.79      |
| lidar       |           28 | $245.30     |
| motor       |           63 | $52.99      |
| sensor      |           29 | $21.45      |
| gyroscope   |           54 | $132.88     |
| gearbox     |           51 | $310.60     |
| regulator   |           95 | $27.14      |
| controller  |           77 | $89.53      |

This stock table should be stored in aligned lists that represent the current stock, just as in task 2.1-3. As well as these variables, you should also represent the following table in a variable called models. 

| Part       |   R1 |   R2 |   R3 |   R4 |
|------------|------|------|------|------|
| servo      |    4 |    7 |    3 |    1 |
| lidar      |    6 |    0 |    6 |    6 |
| motor      |    5 |    4 |    2 |    3 |
| sensor     |    4 |    4 |    7 |    6 |
| gyroscope  |    0 |    0 |    7 |    4 |
| gearbox    |    2 |    6 |    4 |    5 |
| regulator  |    2 |    5 |    4 |    2 |
| controller |    7 |    5 |    4 |    7 |

The variable models should contain a dictionary where the key of the dictionary is the name of the model and the value is the list from subtask 2.2-3, that is aligned with the stock lists, and contains the number of each part required to construct the model.

You should also have a variable called queue which contains the order queue. The order queue is a list of tuples of size two where the first element is the name of the model to be built, and the second element is the number of that given model that are required. A sample order queue is specified below.

("R4",2)
("R1",2)
("R3",1)
("R2",4)
("R1",1)
("R4",2)
("R2",3)

The program then processes the orders, one model at a time. Before building each robot, you must check the feasibility across all parts. If the robot can be feasibly constructed, given the inventory, then the stock is decremented and the build report (which tracks how many robots were built and the expected revenue) is updated. If the robot cannot be constructed, then the robot is put on backorder.

The program then prints a report containing the number of built robots, per model, and the total revenue. The report should also contain the number of each model on backorder and the remaining inventory.

Examples:

Constructed units
R1: 2
R2: 2
R3: 0
R4: 2

Total cost: $21719.82

Backorder
R1: 1
R2: 5
R3: 1
R4: 2

Inventory
servo: 18
lidar: 4
motor: 39
sensor: 1
gyroscope: 46
gearbox: 25
regulator: 77
controller: 39

/////////////////////////////////////////////////////////////////////////////////////////////////////

Task 3 - Mini-API with CLI (Assessed)
Now that you have completed the warm-up, you decide that it is time to put all your hard work together. To do this you need only extend the functionality already described in tasks 3.1-2. You are told to use the current data as specified for by your boss in task 1.

The API
You decide on the following API:

get_model_cost(model, catalog, models): This function should return the cost required to construct the model given the catalog and models dictionaries. These variables should be local to the scope of the function during the function call, not global to the program.

can_build_one(model, inventory, models): This function should return True if the model can be build, given the available inventory. It should return False otherwise.

build_one(model, inventory, catalog, models): This function should decrement the inventory and return the cost of the model. If the model cannot be built then the inventory should not be modified and a cost of $0.00 should be returned.

process_order(model, count, inventory, catalog, models): This function should attempt to fill an order and in doing so return a tuple of size 3 containing the number of constructed models, the number of models to be placed on backorder, and the cost of the constructed models.

apply_discount(total): This function should return the new total after applying the discount as defined in task 2.

CLI Menu
You decide to build a thin CLI wrapper. This should allow users to interact with the system and act on the data that was specified. Your program should display the following menu:

1) Show models and costs
2) Attempt order
3) Show inventory
0) Exit

The menu should ask the user to input an integer. That integer is used to carry out the task. In the case of option (2) the user should be prompted for more information, first the model as a string and then the quantity as an integer.

All integers should have their bounds checked. You do not need to perform type validation. If we tell you that the input has a specific type, you can assume that to be the case.

Example:

1) Show models and costs
2) Attempt order
3) Show inventory
0) Exit

Please enter an integer between (0-3): 1
R1: $3279.90
R2: $3016.24
R3: $4483.54
R4: $4563.77

1) Show models and costs
2) Attempt order
3) Show inventory
0) Exit

Please enter an integer between (0-3): 2
Please enter a model number: R2
Please enter the number of R2 units you would like: 7

Attempting to order models...

R2 order details.
Units built: 6
Units on backorder: 1

Subtotal: $18097.44
Discount (dollars): $2714.62
Total: $15382.82

1) Show models and costs
2) Attempt order
3) Show inventory
0) Exit

Please enter an integer between (0-3): 3
Current inventory:

servo: 0
lidar: 28
motor: 39
sensor: 5
gyroscope: 54
gearbox: 15
regulator: 65
controller: 47

1) Show models and costs
2) Attempt order
3) Show inventory
0) Exit

Please enter an integer between (0-3): 0

NOTE: The code should demonstrate good separation of responsibility. This means that the API functions should not interact with the console, so no input or print statements. You are welcome to use as many functions for the CLI as you would like, but these functions must use the API wherever possible.