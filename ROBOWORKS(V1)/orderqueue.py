# Lists of stock details, that contains part name, part stock, and each part's cost.
part_name = ['servo', 'lidar', 'motor', 'sensor', 'gyroscope', 'gearbox', 'regulator', 'controller']
part_stock = [42,28,63,29,54,51,95,77]
part_cost = [38.79, 245.30, 52.99, 21.45, 132.88, 310.60, 27.14, 89.53]

# Models dictionary that defines the number of required equipments for each robot.
models ={
        "R1": [4,6,5,4,0,2,2,7],
        "R2": [7,0,4,4,0,6,5,5],
        "R3": [3,6,2,7,7,4,4,4],
        "R4": [1,6,3,6,4,5,2,7]
}

# Initialize the dictionary of constructed units and backorder.
constructed_units = {"R1":0, "R2":0, "R3":0, "R4":0}
backorder = {"R1":0, "R2":0, "R3":0, "R4":0}
total_cost = 0

# Inserting the queue (model_name, quantity) of Robots ordered by client.
queue = [("R4",2),("R1",2),("R3",1),("R2",4),("R1",1),("R4",2),("R2",3)]

# Process each order in the queue one unit at a time.
for model_name, quantity in queue:
    for i in range(quantity):
        required_parts = models[model_name]

        # Check the model able to build or not.
        feasible = True
        for j in range(len(part_name)):
            if part_stock[j] < required_parts[j]:
                feasible = False
                break
        
        # If feasible, deduct stock and update total cost and constructed units.
        if feasible:
            for k in range(len(part_name)):
                part_stock[k] -= required_parts[k]
                total_cost += required_parts[k] * part_cost[k]

            constructed_units[model_name] += 1
        else:
            backorder[model_name] += 1

# Output
print("Constructed units")
for model in models:
    print(f"{model}: {constructed_units[model]}")

print()
print(f"Total cost: ${total_cost:.2f}")
print()

print("Backorder")
for model in models:
    print(f"{model}: {backorder[model]}")

print()
print("Inventory")
for n in range(len(part_name)):
    print(f"{part_name[n]}: {part_stock[n]}")

