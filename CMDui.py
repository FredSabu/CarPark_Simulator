"""
This is the View component of the MVC architecture, responsible for handling all the  user-interface-related
functions in the CMD version of the program. It acts as a bridge between the user and the application's core logic,
facilitating user interactions and displaying relevant information from the Model.

This separation of concerns ensures that the user interface logic is decoupled from the business logic, thereby
enhancing the maintainability and scalability of the application.
"""

from CarPark import Model
from CarPark import InterfaceController


class CMDView:
    def __init__(self, model):
        self.model = model

    def display_message(self, message):
        print(message)
    # This method displays all the message to the user. It takes the parameter "message" and print out the contents of
    # the message.

    def get_input(self, prompt):
        return input(prompt)
    # This method gets all the input from the user. It takes the parameter "prompt" and displays the prompt using the
    # input function.


if __name__ == "__main__":
    model = Model(5, "ParkingRecords.csv")
    view = CMDView(model)
    controller = InterfaceController(model, view)
    # Capacity and File Name can be set here

    while True:
        print(f"\nWelcome to the Car Park. At any stage, enter '0' to go back to the main menu.")
        print("\n1. Enter the car park (Hourly rate: £2)")
        print("2. Exit the car park")
        print("3. View available parking spaces")
        print("4. Query Parking record by ticket number")
        print("5. Quit")

        user_input = view.get_input("\nPlease enter your choice: ")

        if user_input == "1":
            registration_number = view.get_input("Please enter the vehicle's registration: ")
            controller.handle_enter_car_park(registration_number)
        elif user_input == "2":
            registration_exit = view.get_input("Please enter the vehicle's registration: ")
            controller.handle_exit_car_park(registration_exit)
        elif user_input == "3":
            controller.handle_view_parking_spaces()
        elif user_input == "4":
            ticket_number = view.get_input("Please enter the ticket number to query: ")
            controller.handle_query_parking_record(ticket_number)
        elif user_input == "5":
            view.display_message("\nThank you for parking with us. Goodbye.")
            break
        else:
            view.display_message("\nInvalid option. Please select a valid option.")
    # Presents options to the user and handles the user input.
