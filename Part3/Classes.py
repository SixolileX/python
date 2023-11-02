
import csv
import decimal
import locale
from datetime import datetime

REGION_CODES = {'w': 'West', 'm': 'Mountain', 'c': 'Central', 'e': 'East'}

class SalesData:
    def __init__(self):
        self.data = []

    def import_sales(self, file_name):
        try:
            parts = file_name.split('_')
            if len(parts) == 4 and parts[0] == 'sales' and parts[3].endswith('.csv'):
                quarter = parts[1]
                year = parts[2]
                region_code = parts[3].split('.')[0]

                if quarter[0] == 'q' and quarter[1:].isdigit():
                    quarter = int(quarter[1:])
                else:
                    raise ValueError("Invalid quarter format")

                if year.isdigit() and len(year) == 4:
                    year = int(year)
                else:
                    raise ValueError("Invalid year format")

                if len(region_code) == 1 and region_code.isalpha():
                    region = REGION_CODES.get(region_code.lower(), 'Unknown')
                else:
                    raise ValueError("Invalid region code format")

                with open(file_name, 'r') as file:
                    reader = csv.DictReader(file)
                    total_amount = 0
                    for row in reader:
                        row['Amount'] = decimal.Decimal(row['Amount'])
                        self.data.append(row)
                        date = row['Date']
                        formatted_amount = locale.currency(row['Amount'], grouping=True)
                        print("{:<15} {:<10} {:<10} {:<10}".format(date, quarter, region, formatted_amount))
                        total_amount += row['Amount']
                    formatted_total = locale.currency(total_amount, grouping=True)
                    print("TOTAL: {:>40}".format(formatted_total))
                    print(f"Imported sales added to list (Quarter: Q{quarter}, Year: {year}, Region: {region_code.upper()})")
                    
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
        except ValueError as ve:
            print(f"Error parsing file name: {ve}")
        except Exception as e:
            print(f"Error importing sales data: {e}")

class Region:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return f"{self.code}: {self.name}"

class Regions:
    def __init__(self):
        self.regions = []

    def add_region(self, region):
        self.regions.append(region)

    def get_region_by_code(self, code):
        for region in self.regions:
            if region.code == code:
                return region

    def valid_region_codes(self):
        return [region.code for region in self.regions]

    def __str__(self):
        return ", ".join([str(region) for region in self.regions])

class File:
    def __init__(self, filename, region):
        self.filename = filename
        self.region = region

    def get_region_code_from_filename(self):
        parts = self.filename.split('_')
        if len(parts) == 4 and parts[0] == 'sales' and parts[3].endswith('.csv'):
            return parts[3].split('.')[0].lower()
        return None

    def is_valid_filename(self):
        return self.get_region_code_from_filename() == self.region.code

    def expected_naming_convention(self):
        return f"sales_Q{self.region.code.upper()}_YYYY.csv"

class DSales:
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, date, region, amount):
        self.date = datetime.strptime(date, self.DATE_FORMAT)
        self.region = region
        self.amount = amount
        self.calculate_quarter()

    def calculate_quarter(self):
        month = self.date.month
        if month in [1, 2, 3]:
            self.quarter = 1
        elif month in [4, 5, 6]:
            self.quarter = 2
        elif month in [7, 8, 9]:
            self.quarter = 3
        else:
            self.quarter = 4

    def to_list(self):
        return [self.date.strftime(self.DATE_FORMAT), self.quarter, self.region.code, self.amount]

    def is_valid(self):
        return isinstance(self.date, datetime) and self.amount > 0

class Sales:
    def __init__(self):
        self.sales = []

    def add_sales(self, sales):
        self.sales.append(sales)

    def get_sales_by_index(self, index):
        if 0 <= index < len(self.sales):
            return self.sales[index]

    def add_sales_list(self, other_sales_list):
        self.sales.extend(other_sales_list.sales)

    def __len__(self):
        return len(self.sales)

    def __iter__(self):
        return iter(self.sales)

    def has_bad_data(self):
        for sales in self.sales:
            if not sales.is_valid():
                return True
        return False

class FileImportError(OSError):
    pass
