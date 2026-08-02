###############################
# Place your data model here. #
###############################
'''
      PART INVENTORY AND PRICING TABLE (REFERENCE)
      ____________________________________________
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
      |_____________|______________|_____________|
'''
PRICE_CATALOG = {
    "servo": 38.79,
    "lidar": 245.30,
    "motor": 52.99,
    "sensor": 21.45,
    "gyroscope": 132.88,
    "gearbox": 310.60,
    "regulator": 27.14,
    "controller": 89.53
}

MODELS = {
    "R1":{"servo": 4,
          "lidar": 6,
          "motor": 5,
          "sensor": 4,
          "gyroscope": 0,
          "gearbox": 2,
          "regulator": 2,
          "controller": 7},
    "R2":{"servo": 7,
          "lidar": 0,
          "motor": 4,
          "sensor": 4,
          "gyroscope": 0,
          "gearbox": 6,
          "regulator": 5,
          "controller": 5},
    "R3":{"servo": 3,
          "lidar": 6,
          "motor": 2,
          "sensor": 7,
          "gyroscope": 7,
          "gearbox": 4,
          "regulator": 4,
          "controller": 4},
    "R4":{"servo": 1,
          "lidar": 6,
          "motor": 3,
          "sensor": 6,
          "gyroscope": 4,
          "gearbox": 5,
          "regulator": 2,
          "controller": 7}
}

inventory = {
          "servo": 42,
          "lidar": 28,
          "motor": 63,
          "sensor": 29,
          "gyroscope": 54,
          "gearbox": 51,
          "regulator": 95,
          "controller": 77
}

# Discount thresholds will be used to apply discount.
high_discount_threshold = 1500
mid_discount_threshold = 1000
low_discount_threshold = 300

high_discount_rate = 0.15
mid_discount_rate = 0.10
low_discount_rate = 0.05

################################
# Place your API methods here. #
################################
def get_model_cost(model: str, catalog: dict, models: dict) -> float:
      '''
      Calculate the total cost of building a given model.

      Parameters:
            model (str): Model name (e.g., "R1").
            catalog (dict): Model parts price catalog.
            models (dict): Models dictionary with its parts requirements.
      
      Returns:
            Gives the total cost of model building.
      
      '''
      total = 0
      for part, quantity in models[model].items():
            total += catalog[part] * quantity
      return total

def can_build_one(model: str, inventory: dict, models: dict) -> bool:
      '''
      Identify the ability to make a model by parts stock.

      Parameters:
            model (str): Model name (e.g., "R1").
            inventory (dict): Model parts stock.
            models (dict): Models dictionary with its parts requirements.
      
      Returns:
            Returns in boolean values. If model can be make-True, else False.
      '''
      for part, quantity in models[model].items():
            if inventory.get(part)<quantity:
                  return False
      return True

def build_one(model: str, inventory: dict, catalog: dict, models: dict) -> float:
      '''
      Start to make the model by using appropreate parts and managing model parts stock, if possible to make it.

      Parameters:
            model(str): Model name (e.g., "R1").
            inventory(dict): Model parts stock.
            catalog(dict): Model parts price catalog.
            models (dict): Models dictionary with its parts requirements.

      Returns:
            Returns the value of total cost to build model. 
      '''
      if not can_build_one(model, inventory, models):
            return 0.0
      for part, quantity in models[model].items(): #
            inventory[part] -= quantity

      return get_model_cost(model, catalog, models)

def process_order(model: str, count: int, inventory: dict, catalog: dict, models: dict) -> tuple:
      '''
      Function processes an order for given model.

      Parameters:
            model(str): Model name (e.g., "R1").
            count(int): Number of units requested.
            inventory(dict): MOdels part stock.
            catalog(dict): Model parts price catalog.
            models(dict): Models dictionary with its parts requirements.
      
      Returns:
            tuple:(built, backorder, total) => (built units, backorder units, total cost).
      '''
      built = 0
      total = 0
      for _ in range(count):
            if can_build_one(model, inventory, models):
                  total += build_one(model, inventory, catalog, models)
                  built += 1
            else:
                  continue
            
      backorder = count - built

      return (built, backorder, total)

def apply_discount(total: float) -> float:
    '''
    Apply discount to the total cost based on predefined thresholds.
    
    Parameters: 
        total (float): Total cost before discount.

    Returns:
        float: Final cost after applying the discount.
    '''

    if total > high_discount_threshold:
        return total * (1 - high_discount_rate)
    elif total > mid_discount_threshold:
        return total * (1 - mid_discount_rate)
    elif total > low_discount_threshold:
        return total * (1 - low_discount_rate)
    else:
        return total

########################################
# Place your CLI code and methods here #
########################################

def show_models() -> str:
      '''
      Function help to show each model name with cost.
      '''
      for model in MODELS:
            cost = get_model_cost(model, PRICE_CATALOG, MODELS)
            print(f"{model}: ${cost:.2f}")
      
def show_inventory() -> str:
      '''
      Displays the current product inventory.
      '''
      print("Current inventory:")
      print()
      for part, quantity in inventory.items():
            print(f"{part}: {quantity}")

def attempt_order() -> str:
      '''
      Allows to the customer for ordering particular Model R_.
      '''
      model = input("Please enter a model number: ")
      count = int(input(f"Please enter the number of {model} units you would like: \n"))

      print("Attempting to order models...")
      print()

      built, backorder, subtotal = process_order(model, count, inventory, PRICE_CATALOG, MODELS)

      total = apply_discount(subtotal)
      discounted_amount = subtotal - total

      print(f"{model} order details.")
      print(f"Units built: {built}")
      print(f"Units on backorder: {backorder}")
      print()

      print(f"Subtotal: ${subtotal:.2f}")
      print(f"Discount (dollars): ${discounted_amount:.2f}")
      print(f"Total: ${total:.2f}")


# Main function of the program.
def main():
      while True:
            print("1) Show models and costs")
            print("2) Attempt order")
            print("3) Show inventory")
            print("0) Exit")
            print()
            click = int(input("Please enter an integer between (0-3): "))
            if click < 0 or click > 3:
                  print("Invalid option. Try again.")
                  print()
                  continue

            if click == 1:
                  show_models()

            elif click == 2:
                  attempt_order()

            elif click == 3:
                  show_inventory()

            elif click == 0:
                  break

            print()

# execute entire system.
main()



