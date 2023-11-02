

from Classes import SalesData, Region, Regions, File, FileImportError
from Part3.Userfunctions import FileImportError, save_sales, load_data

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
            .
if __name__ == "__main__":
    main_menu()
