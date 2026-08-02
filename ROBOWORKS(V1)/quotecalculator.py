# Preset thresholds for discount calculation.
high_discount_threshold = 1500
mid_discount_threshold = 1000
low_discount_threshold = 300

high_discount_rate = 0.15
mid_discount_rate = 0.10
low_discount_rate = 0.05


# Required variable names (Do Not Change)
product_name = ["motor", "sensor", "frame", "cpu"]
product_price = [49.99, 15.75, 120.00, 85.50]

def product_cart(product_name: list) -> list:
    '''
    Function inputs the exact quantity of each product.

    Parameters:
        product_name(list): defines all items of the product.

    Returns:
        list: Quantities of each product.
    '''
    quantity = []
    for i in range(len(product_name)):
        quantity_value = int(input(f"{product_name[i]}: "))
        if quantity_value < 0:
            print("Please enter appropriate quantity properly!")
        else:
            quantity.append(quantity_value)
    return quantity

def product_quote(product_name: list, quantity: list, product_price: list) -> list:
    '''
    Display exact calculations of price for each product.

    Parameters: 
        product_name(list): list of all items of the product.
        quantity(list): list of product requirement quantity.
        product_price(list): list of all product price.

    Returns:
        list: Function returns quantity of each product.
    '''
    price = []
    for j in range(len(product_name)):

        # line_total defines total price of each product by quantity.
        line_total = quantity[j] * product_price[j]
        price.append(line_total)

        print(f"{product_name[j]}: {quantity[j]} x ${product_price[j]:.2f} = ${line_total:.2f}")

    return price

def discount(price: list) -> float:
    '''
    Calculate discount based on subtotal.
        Logic: discount= subtotal * ((__)% / 100)

    Parameters:
        price (list): list of price according to products quantity.

    Returns:
        float: Discounted amount.
    '''

    subtotal = sum(price)
    if subtotal > high_discount_threshold:
        discount = subtotal * (high_discount_rate)
        return discount
    elif subtotal > mid_discount_threshold:
        discount = subtotal * (mid_discount_rate)
        return discount
    elif subtotal > low_discount_threshold:
        discount = subtotal * (low_discount_rate)
        return discount
    else:
        discount = 0.0
        return discount

def display_bill(subtotal: float, discount: float) -> str:
    '''
    It will be displaying Subtotal, Dicount and Total amount to pay, that has been calculated.
    
    Parameters:
        subtotal(float): subtotal amount calculated before.
        discount(float): value of dicount on subtotal.

    Returns:
        str: returns values of subtotal, discount, and total in formatted string.
    '''

    total = subtotal - discount
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Discount: ${discount:.2f}")
    print(f"Total: ${total:.2f}")


# ------- Main Program --------

print("Welcome to the RoboWorks Quote Calculator.\n")
print("For each product below, please specify your required quantity.\n")

# calling function product_cart.
quantity = product_cart(product_name)

print("\nPlease see your quote below.\n")

# calling function product_quote.
price = product_quote(product_name, quantity, product_price)
print()

# Print summary of entire purchase bill.
subtotal = sum(price)
disc = discount(price)
display_bill(subtotal, disc)

    

