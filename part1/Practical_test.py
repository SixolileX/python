import csv
import os
import decimal
import locale

# for cur4rency
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

sales_data = []

# adding dta
def add_sales():
    while True:
        try:
            amount = decimal.Decimal(input("Enter sales amount: "))
            year = int(input("Enter year: "))
            month = int(input("Enter month (1-12): "))
            day = int(input("Enter day (1-31): "))

            if year < 2000 or year > 9999:
                raise ValueError("Year must be between 2000 and 9999")

            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12")

            if month == 2 and (day < 1 or day > 31):
                raise ValueError(" day must be between 1 and 31")

            #  quarter
            if month in [1, 2, 3]:
                quarter = 1
            elif month in [4, 5, 6]:
                quarter = 2
            elif month in [7, 8, 9]:
                quarter = 3
            else:
                quarter = 4

            sales_data.append({
                'Amount': amount,
                'Year': year,
                'Month': month,
                'Day': day,
                'Quarter': quarter
            })

            date = f"{year}-{month:02d}-{day:02d}"
            print()
            print("Sales for {} added to list",date)
 
            main_menu()

        except (ValueError, decimal.InvalidOperation) as e:
            print(f"Error: {e}")
            continue

# import data
def import_sales(filename):
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            print("{:<4} {:<15} {:<10} {:<10}".format("", "Date", "Quarter", "Amount"))
            print("--------------------------------------------")
            for i, row in enumerate(reader, start=1):
                amount = locale.currency(decimal.Decimal(row['Amount']), grouping=True)
                year = int(row['Year'])
                month = int(row['Month'])
                day = int(row['Day'])
                date = f"{year}-{month:02d}-{day:02d}"
                quarter = row['Quarter']
                sales_data.append({
                    'Amount': decimal.Decimal(row['Amount']),
                    'Year': year,
                    'Month': month,
                    'Day': day,
                    'Quarter': quarter
                })
                print("{:<4} {:<15} {:<10} {:<10}".format(i, date, quarter, amount))

        print("--------------------------------------------")
        total_amount = sum(entry['Amount'] for entry in sales_data)
        print("TOTAL: {:>35}".format(locale.currency(total_amount, grouping=True)))
        print("Imported sales added to list")

    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    except Exception as e:
        print(f"Error: {e}")

# display data
def display_sales():
    if not sales_data:
        print("No sales data available.")
    else:
        print("{:<4} {:<15} {:<10} {:<10}".format("", "Date", "Quarter", "Amount"))
        print("--------------------------------------------")
        total_amount = 0
        for i, entry in enumerate(sales_data, start=1):
            amount = locale.currency(entry['Amount'], grouping=True)
            year = entry['Year']
            month = entry['Month']
            day = entry['Day']
            date = f"{year}-{month:02d}-{day:02d}"
            quarter = entry['Quarter']
            print("{:<4} {:<15} {:<10} {:<10}".format(i, date, quarter, amount))
            total_amount += entry['Amount']

        print("--------------------------------------------")
        print("TOTAL: {:>35}".format(locale.currency(total_amount, grouping=True)))

# save data
def save_sales():
    try:
        with open('regional_sales.csv', mode='w', newline='') as file:
            fieldnames = ['Amount', 'Year', 'Month', 'Day', 'Quarter']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sales_data)
        print()
        print("Sales data saved to 'regional_sales.csv'.")
        print("Bye!")

    except Exception as e:
        print(f"Error saving sales data: {e}")

# Main menu 
def main_menu():
    while True:
        print("\nCOMMAND MENU")
        print("view    - View All Sales")
        print("add     - Add Sales")
        print("import  - Import Sales from File")
        print("menu    - Show Menu")
        print("exit    - Exit Program")
        print()
        choice = input("Enter your Command: ")

        if choice == "add":
            add_sales()
        elif choice == "import":
            filename = input("Please enter the name of the file to import: ")
            import_sales(filename)
        elif choice == "view":
            display_sales()
        elif choice == "menu":
            main_menu()
        elif choice == "exit":
            save_sales()
            break
        else:
            print("Please try again.")

if __name__ == "__main__":
   # it was giving errors when i created a function so i manage to make the read like this 
    if os.path.exists('regional_sales.csv'):
        with open('regional_sales.csv', mode='r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                sales_data.append({
                    'Amount': decimal.Decimal(row['Amount']),
                    'Year': int(row['Year']),
                    'Month': int(row['Month']),
                    'Day': int(row['Day']),
                    'Quarter': row['Quarter']
                })

    main_menu()
