
import decimal
import locale
import csv
from Classes import SalesData, FileImportError
sales_data = []

def display_sales():
    print("{:<15} {:<10} {:<10} {:<10}".format("Date","Quarter","Region",  "Amount"))
    print("--------------------------------------------")
    total_amount = 0
    for entry in sales_data:
        date = entry['Date']
        region = entry['Region']
        quarter = entry['Quarter']
        amount = entry['Amount']
        total_amount += amount
        formatted_amount = locale.currency(amount, grouping=True)
        print("{:<15} {:<10} {:<10} {:<10}".format(date,quarter, region,  formatted_amount))
    print("--------------------------------------------")
    formatted_total = locale.currency(total_amount, grouping=True)
    print("TOTAL: {:>40}".format(formatted_total))
    
def save_sales(file_name, sales_data):
    try:
        with open(file_name, 'w', newline='') as file:
            fieldnames = ['Date', 'Quarter','Region', 'Amount']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for sales in sales_data.data:
                writer.writerow(sales)
        print("Bye!")
    except Exception as e:
        print(f"Error saving sales data: {e}")

#loading data

def load_data(file_name, sales_data):
    try:
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['Amount'] = decimal.Decimal(row['Amount'])
                sales_data.add_sales(row['Date'], row['Region'], row['Amount'])
    except FileNotFoundError:
        raise FileImportError(f"File '{file_name}' not found.")
    except Exception as e:
        raise FileImportError(f"Error loading sales data: {e}")
