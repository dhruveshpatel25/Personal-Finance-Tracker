from datetime import datetime

date_format="%d-%m-%Y"

CATEGORIES={
    "I":"Income",
    "E":"Expense"
}

#get the date from the user
def get_date(prompt,allow_default=False):

    #take the input from user for date
    date_str=input(prompt)

    #if user presses enter and allow_default is True, return today's date
    if allow_default and not date_str:

        #return today's date in the specified format
        return datetime.now().strftime(date_format)
    
    try:

        #convert the string into date time object
        valid_date=datetime.strptime(date_str,date_format)

        #return the date in the specified format
        return valid_date.strftime(date_format)
    except ValueError:

        #if the date is not in the specified format, catch the ValueError and print the error message
        print("Invalid date format. Please use DD-MM-YYYY")

        #and call the function recursively
        return get_date(prompt,allow_default)
    
#get the amount from the user
def get_amount():
    try:

        #take the input from the user for amount
        amount=float(input("Enter the amount: "))

        #check if the amount is greater than 0
        if amount<=0:

            #if less raise error
            raise ValueError("Amount must be greater than 0")
        
        #if greater return the amonunt
        return amount
    except ValueError as e:

        #if the amount is not a valid number, catch the ValueError and print the error message
        print(e)

        #and call the function recursively
        return get_amount()
    
#get category from the user
def get_category():

    #take the input from the user for category
    category=input("Enter the category('I' for Income or 'E' for Expense): ").upper()

    #check if the category is in the CATEGORIES dictionary
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    #if not, print the error message
    print("Invalid category. Please enter 'I' or 'E'")

    #and call the function recursively
    return get_category()

#get description from the user
def get_description():

    #take the input from the user for description
    return input("Enter a description: ")