import csv
import decimal
import locale


REGION = {'w': 'West', 'm': 'Mountain', 'c': 'Central', 'e': 'East'}


locale.setlocale(locale.LC_ALL, '')


sales_data = []

#Import
def import_sales(file_name):
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
                region = REGION.get(region_code.lower(), 'Unknown')
            else:
                raise ValueError("Invalid region code format")

            with open(file_name, 'r') as file:
                reader = csv.DictReader(file)
                total_amount = 0
                print("{:<15} {:<10} {:<10} {:<10}".format("Date", "Quarter", "Region", "Amount"))
                print("--------------------------------------------")
                for row in reader:
                    row['Amount'] = decimal.Decimal(row['Amount'])
                    sales_data.append(row)
                    date = row['Date']
                    formatted_amount = locale.currency(row['Amount'], grouping=True)
                    print("{:<15} {:<10} {:<10} {:<10}".format(date, quarter, region, formatted_amount))
                    total_amount += row['Amount']
                print("--------------------------------------------")
                formatted_total = locale.currency(total_amount, grouping=True)
                print("TOTAL: {:>40}".format(formatted_total))
                print(f"Imported sales added to list (Quarter: Q{quarter}, Year: {year}, Region: {region_code.upper()})")
                
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except ValueError as ve:
        print(f"Error parsing file name: {ve}")
    except Exception as e:
        print(f"Error importing sales data: {e}")

        
        
# add sales
def add_sales(sales_data):
    date = input("Enter the date (YYYY-MM-DD): ")
    region = input("Enter the region (w/m/c/e): ").lower()
    
   
    amount = int(input("Enter the sales amount: "))
    
   
    year, month, day = map(int, date.split('-'))
    
  #quarter
    if month in [1, 2, 3]:
        quarter = 1
    elif month in [4, 5, 6]:
        quarter = 2
    elif month in [7, 8, 9]:
        quarter = 3
    else:
        quarter = 4
    
    new_data = {
        'Date': date,
        'Region': REGION.get(region, 'Unknown'),
        'Quarter': quarter, 
        'Amount': amount,
    }
    sales_data.append(new_data)
    
def save_sales(file_name):
    try:
        with open(file_name, 'w', newline='') as file:
            fieldnames = ['Date', 'Quarter','Region', 'Amount']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sales_data)
        print("Bye!")
    except Exception as e:
        print(f"Error saving sales data: {e}")

#displaying 
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
    
def main_menu():
    while True:
        print("\nCOMMAND MENU")
        print("view    - View All Sales")
        print("add     - Add sales")
        print("import  - Import sales from file")
        print("menu    - Show Menu")
        print("exit    - Exit program")
        print()
        choice = input("Enter your Command : ")

        if choice == "add":
            add_sales(sales_data)
        elif choice == "import":
            filename = input("Please enter name of file to import: ")
            import_sales(filename)
        elif choice == "view":
            display_sales()
        elif choice == "menu":
            main_menu()
        elif choice == "exit":
            save_sales('sales_q1_2021_z.csv')
            break
        else:
            print("Please try again.")

#loading data
def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['Amount'] = decimal.Decimal(row['Amount'])
                sales_data.append(row)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"Error loading sales data: {e}")

if __name__ == "__main__":
    load_data('sales_q1_2021_z.csv')
    main_menu()