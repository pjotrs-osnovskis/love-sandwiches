"""
First I used pip3 install gspread google-auth command in VSCode terminal to install gspread library
Then importing gspread
"""
import gspread

# Then used this line to access Credentials class
from google.oauth2.service_account import Credentials

# Installing pprint to show data in more readable format
from pprint import pprint


# Here we use constant SCOPE (constants written in CAPITAL LETTERS) to access certain google services
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Passing creds.json file for credentials to work
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# GSPREAD client
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Accessing Love Sandwiches spreadsheet
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

# Testing connection to spreadsheet
# sales = SHEET.worksheet("sales")
# data = sales.get_all_values()
# print(data)

def get_sales_data():
    """
    Get sales figures input from user.
    Run while loop to collect a valid string of data from the user
    via terminal, which must be a string of 6 numbers separated
    by commas. The loop will run until correct data is entered.
    """

    while True:
        print("Please enter sales data from the last market")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")
        # Check if it's working
        # print(f"The data provided is {data_str}")

        sales_data = data_str.split(",")
        # Check if it's working
        # print(sales_data)

        if validate_data(sales_data):
            print("Success!\n")
            break
    return sales_data


# Data validation
def validate_data(values):
    """
    Inside the try, it converts all string values to ints.
    Shows ValueError if strings cant be converted in to int,
    or if there aren't 6 values entered.
    """
    # Check if it's working
    # print(values)

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"6 values required, you provided: {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please check data and try again.\n")
        return False
    return True

# This is old code and new refactoring code added to update_worksheet function
# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully.\n")

# def update_surplus_worksheet(data):

#     """
#     Update surplus worksheet, add new row with the list data provided
#     """  

#     print("Updating surplus worksheet...\n")
#     sales_worksheet = SHEET.worksheet("surplus")
#     sales_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted in to a relevant worksheet
    Updates relevant worksheet with data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")



def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste.
    - Negative surplus indicates extra made when stock ran out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entires_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwitch and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%.
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    print(f"{new_surplus_data}\n")
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entires_sales()
    stock_data = calculate_stock_data(sales_columns)
    print(f"{stock_data}\n")
    update_worksheet(stock_data, "stock")

# Calling main() function
print("Welcome to Love Sandwiches Data Automation!\n")
main()
