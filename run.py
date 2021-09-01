"""
First I used pip3 install gspread google-auth command in VSCode terminal to install gspread library
Then importing gspread
"""
import gspread

# Then Used this line to access Credentials class
from google.oauth2.service_account import Credentials

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

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with th list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)


