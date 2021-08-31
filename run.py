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
    """
    print("Please enter sales data from the last market")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here:")
    print(f"The data provided is {data_str}")

# Calling get_sales_data function
get_sales_data()