"""
As introduced in System Design Lecture 5, I am following the Model-View-Controller Software Architecture. I have used
the MVC architecture as it optimises partitioning and abstraction while providing a clear separation of concerns.

- Model: Manages data and business logic. In this project, the Model is responsible for the efficient handling of
parking data, leveraging binary search for quick data retrieval and processes such as managing parking spaces.

- View: Handles user interface. The project includes distinct Views for CMD and GUI, tailored to different user
interfaces but sharing the same underlying logic, this means that there is almost zero repeated code.

- Controller: Acts as the intermediary between the Model and View, implementing the core logic for vehicle management
within the program.

This architecture enhances maintainability, as each component can be modified independently. It supports
flexibility and extensibility, allowing easy integration of new features. Robustness is achieved through
decoupled design, isolating changes and failures to individual components. Performance is optimised in each
component via the use of binary search and indexing.
"""

import csv
import time
import random
import re
from datetime import datetime


"""
I have implemented a binary search for efficient data retrieval. This method significantly 
reduces the time complexity of search operations from O(n) to O(log n), where n is the number of records in the 
dataset. This will improve performance especially on larger datasets. I have implemented this with scalability in mind.

I have a normal binary search (binary_search) for entry and querying.
I also have adapted binary search (binary_search_latest) for exiting the car park. This is if a car (same registration)
has entered the car park multiple times, when exits, the binary search retrieves the latest entry to avoid errors. 
It is part of the 'Model' in my MVC architecture, but I have separated it here for clarity and single responsibility.
"""


class BinarySearch:
    @staticmethod
    def binary_search_helper(data_list, target_registration_number, registration_key_function, latest_search=None):
        left, right = 0, len(data_list) - 1

        while left <= right:
            mid = (left + right) // 2
            row = data_list[mid]
            row_key = registration_key_function(row)

            if latest_search:
                process_result = latest_search(row, row_key, target_registration_number)
                if process_result is not None:
                    return process_result

            if row_key < target_registration_number:
                left = mid + 1
            elif row_key > target_registration_number:
                right = mid - 1
            else:
                return row

        return None
    
    # Code for binary search with latest_search parameter that is able to accommodate further searches.

    @staticmethod
    def binary_search_normal(data_list, target_registration_number, registration_key_function):
        return BinarySearch.binary_search_helper(data_list, target_registration_number, registration_key_function)
    # Conducts a standard binary search by calling binary_search_helper

    @staticmethod
    def binary_search_latest(data_list, target_registration_number, registration_key_function):
        def latest_search(row, row_key, target):
            if row_key == target and not row[4]:
                return row
            return None

        return BinarySearch.binary_search_helper(data_list, target_registration_number, registration_key_function,
                                                 latest_search)
    # Conducts a binary search that returns the latest registration, once again by calling binary_search_helper.


"""
DataHandler class handles operations related to a data file. This class encapsulates file operations, providing an 
interface for creating, reading, and updating the data file. It is part of the 'Model' but I have separated it here for 
clarity and single responsibility. I have also included error handling for file-related operations
"""


class DataHandler:
    def __init__(self, data_file):
        self.data_file = data_file
        self.file_creation_status = self.create_data_file()

    def create_data_file(self):
        try:
            open(self.data_file, 'x').close()
            return 'created'
        except FileExistsError:
            pass
        # Attempts to create a new CSV file. If that file already exists it will do nothing. (Error/Exception handling)
        # Returns "created" status if a new file was created

    def read_car_parking_data(self):
        try:
            with open(self.data_file, "r") as file:
                car_parking_reader = csv.reader(file)
                return list(car_parking_reader)
        except FileNotFoundError:
            return "file_not_found"
        except IOError:
            return "io_error"
        except csv.Error:
            return "csv_error"
        # Opens and reads the data file, returning the data as a list of rows.
        # In any errors occurs, for example, it returns a corresponding error message.(Error/Exception handling)

    def update_car_parking_data(self, car_parking_data):
        try:
            with open(self.data_file, "w", newline="") as update_file:
                car_parking_update = csv.writer(update_file)
                for data_row in car_parking_data:
                    car_parking_update.writerow(data_row)
        except IOError:
            return "io_error"
        except csv.Error:
            return "csv_error"
        # Update existing data in data file with data from car_parking_data.
        # Once again, if any errors occurs,it returns a corresponding error message.(Error/Exception handling)


"""
Main Model class that handles functions such as allocating parking spaces, calculating parking fee and other methods. 
This class as the interface between data and the logic of the program, enhancing separation of concerns. 
"""


class Model:
    def __init__(self, capacity, data_file):
        self.capacity = capacity
        self.data_handler = DataHandler(data_file)
        self.occupied_spaces = set()
        self.parking_index()

    def read_car_parking_data(self):
        return self.data_handler.read_car_parking_data()
    # Delegates the task of reading to the file to the DataHandler class, maintaining separation of concerns.

    def update_car_parking_data(self, car_parking_data):
        self.data_handler.update_car_parking_data(car_parking_data)
    # Delegates the task of writing to the file to the DataHandler class, once again maintaining separation of concerns.

    """
    To further increase efficiency and performance, I use an index to track occupied spaces. When the program starts, it 
    initialises the index by reading the data file ONCE. Whenever a car enters or leaves, the index will be updated 
    accordingly.The indexing improves efficiency by avoiding repeated data file iterations.
    """

    def parking_index(self):
        car_parking_data = self.read_car_parking_data()
        for row in car_parking_data:
            if not row[4]:
                self.occupied_spaces.add(int(row[2]))
    # If there is no exit time [4] ( the car is still parked), then it adds parking space number [2] to occupied_space

    def parking_availability(self):
        return self.capacity - len(self.occupied_spaces)
    # Subtracts occupied spaces from capacity to find how many spaces are available
    # It does NOT represent WHICH specific spaces are available

    def allocate_parking_space(self):
        available_spaces = set(range(1, self.capacity + 1)) - self.occupied_spaces
        return min(available_spaces) if available_spaces else None
    # Finds which specific spaces are available for new cars.
    # Creates a set of parking spaces from 1 to car park capacity and subtracts that from occupied spaces.
    # returns the space with the smallest number.

    def parking_fee(self, entry_time, exit_time):
        entry_datetime = datetime.strptime(entry_time, "%H:%M:%S %Y-%m-%d")
        exit_datetime = datetime.strptime(exit_time, "%H:%M:%S %Y-%m-%d")
        time_difference = exit_datetime - entry_datetime
        hours_parked = time_difference.total_seconds() / 3600
        hourly_rate = 2
        total_fee = hours_parked * hourly_rate
        return total_fee
    # Calculates the difference between entry and exit in hours
    # Multiplies the parking fee (£2) by hours parked and return the total parking fee

    def update_parking_data(self, registration_number, ticket_number, parking_space, entry_time):
        car_parking_data = [registration_number, ticket_number, parking_space, entry_time, None, None]

        car_parking_data_list = self.data_handler.read_car_parking_data()
        car_parking_data_list.append(car_parking_data)

        self.data_handler.update_car_parking_data(car_parking_data_list)

    # Creates a new parking record for each new car entry that includes:
    # registration number, ticket number, parking space, entry time, and placeholders for exit time and fee.
    # Reads existing car parking data, appends the new record, and updates the data file.
    # This ensures that the new entry is stored in the data file.

    def is_already_parked(self, registration_number):
        car_parking_data = self.read_car_parking_data()
        car_parking_data.sort(key=lambda row: row[0].strip().upper())  # Sort by registration number

        def get_registration(row):
            return row[0].strip().upper()

        found_record = BinarySearch.binary_search_normal(car_parking_data, registration_number.upper(),
                                                         get_registration)
        return found_record is not None and not found_record[4]
    # Checks if a car with a given registration number is already parked.
    # Reads car parking data, sorts it by registration number (in uppercase, whitespace trimmed) for binary search.
    # Uses a binary search to find a matching registration number.
    # Returns True if a match is found without an exit time (indicating the car is still parked), otherwise False.

    def find_record_by_ticket(self, ticket_number):
        ticket_search_data = self.read_car_parking_data()
        ticket_search_data.sort(key=lambda row: row[1])

        def get_ticket(row):
            return row[1]
        return BinarySearch.binary_search_normal(ticket_search_data, ticket_number, get_ticket)
    # Finds a parking record based on given ticket number.
    # Data is sorted by ticker number [1] and a binary search is performed.
    # If a matching ticket number is found, the data in the row is returned.


"""
The BaseController class handles the core logic of processing car entries and exits, and delegates data handling to the
Model while using the View for user interaction. Doing this allows me to adhere to the principles of MVC architecture, 
ensuring a clear separation of concerns and enhancing maintainability and scalability of the application.
"""


class BaseController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    """
    start_car_entry_process: Handles the process for a vehicle entering the car park. Registration number is checked for
    using "binary_search_normal" and the process outputs variable statuses depending on outcome. 
    """
    
    def start_car_entry_process(self, registration_number):
        if len(self.model.occupied_spaces) >= self.model.capacity:
            return "full", None
    # Compares occupied spaces with capacity to check to see if the car park is full and returns status

        registration_number = registration_number.upper()
        if self.model.is_already_parked(registration_number):
            return "already_parked", None
    # Checks to see if the car is already parked and returns status.

        parking_space = self.model.allocate_parking_space()
    # Calls on the allocate_parking_space function to assign a parking space for the car.

        if parking_space is not None:
            entry_time = time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())
            ticket_number = registration_number.upper().replace(" ", "") + str(random.randint(1000, 9999))
            self.model.update_parking_data(registration_number, ticket_number, parking_space, entry_time)
            self.model.occupied_spaces.add(parking_space)
            return "entry_success", (parking_space, ticket_number)
    # After successfully assigning a parking space: entry time is recorded, ticket number is generated, parking data
    # is updated and assigned parking space is added to "occupied_spaces".
        else:
            return "full", None
    # Returns status based on outcome.

    def car_entry_reg_check(self, registration_number):
        if not registration_number.strip():
            return "no_registration_entered", None

        if self.model.parking_availability() <= 0:
            return "full", None

        pattern = r'^[A-Z]{2}[0-9]{2}\s[A-Z]{3}$'
        if not re.match(pattern, registration_number.upper()):
            return "invalid_registration", None
        return self.start_car_entry_process(registration_number)
    # Checks for empty registration and parking availability.
    # Uses a regex pattern to validate UK registration number format.
    # Returns status based on outcome.

    def car_entry_status(self, status, result, registration_number):
        if status == 'full':
            return "Sorry, the car park is at maximum capacity currently."
        elif status == 'invalid_registration':
            return "Invalid registration number. Please enter a valid UK registration number. For example: LM55 TCU"
        elif status == 'no_registration_entered':
            return "No registration number entered. Please enter a valid UK registration number. For example: LM55 TCU"
        elif status == 'entry_success':
            parking_space, ticket_number = result
            available_spaces_message = self.view_available_parking()
            return self.car_entry_confirmation(parking_space, ticket_number, available_spaces_message)
        elif status == 'already_parked':
            return f"Vehicle with registration {registration_number} is already parked."
        return None
    # Returns appropriate response based on the status received from the whole car entry process.

    def car_entry_confirmation(self, parking_space, ticket_number, available_spaces_message):
        confirmation_message = "\nYour vehicle has been successfully parked."
        confirmation_message += f"\nAssigned Parking space: {parking_space}"
        confirmation_message += f"\nYour Ticket Number: {ticket_number}"
        confirmation_message += "\nPlease keep your ticket safe."
        confirmation_message += f"\n{available_spaces_message}"
        return confirmation_message
    # Returns parking confirmation message if the status was "success".

    """
    start_car_exit_process: Handles the process for a vehicle entering the exiting park. Registration number is checked 
    for using "binary_search_latest" and this process also outputs variable statuses depending on outcome. 
    """

    def start_car_exit_process(self, registration_exit, car_parking_data):
        registration_exit = registration_exit.strip().upper()
        sorted_data_for_search = sorted(car_parking_data, key=lambda row: row[0].strip().upper())
        found_record = BinarySearch.binary_search_latest(sorted_data_for_search, registration_exit,
                                                         lambda row: row[0].strip().upper())
        if found_record:
            entry_time = found_record[3]
            exit_time = time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())
            parking_charge = self.model.parking_fee(entry_time, exit_time)
            found_record[4] = exit_time
            found_record[5] = "{:.2f}".format(parking_charge)
            self.model.update_car_parking_data(car_parking_data)
            parking_space = int(found_record[2])
            self.model.occupied_spaces.remove(parking_space)
            return "exit_success", found_record, parking_charge
            # If car is still parked, Entry time is retrieved from the record and current time is now the exit time.
            # Parking charge is calculated using the entry time and exit time
            # Parking record is updated with the exit time and parking charge (2 decimal places)
            # Parking space will be removed so that another car can use it. Returns outcome status.
        else:
            return "not_parked", None, None
        # If no matching record is found, returns outcome status.

    def car_exit_status(self, registration_exit):
        exit_message = ""
        if not registration_exit.strip():
            exit_message = "No registration number entered. Please enter a registration number to leave the Car Park."
        else:
            car_parking_data = self.model.read_car_parking_data()
            status, vehicle_record, parking_charge = self.start_car_exit_process(registration_exit, car_parking_data)
            if status == "exit_success":
                self.model.update_car_parking_data(car_parking_data)
                available_spaces_message = self.view_available_parking()
                exit_message = self.car_exit_confirmation(vehicle_record, parking_charge, available_spaces_message)
            elif status == "not_parked":
                exit_message = f"No vehicle with registration {registration_exit} is currently parked"
        return exit_message
    # Checks to see if registration number is entered (not empty value or white space)
    # Returns appropriate response based on the status received from the whole car exit process.

    def car_exit_confirmation(self, vehicle_record, parking_charge, available_spaces_message):
        exit_message = f"\nVehicle with registration {vehicle_record[0]} exited the car park."
        exit_message += f"\nExit time: {vehicle_record[4]}"
        exit_message += f"\nParking Identifier: {vehicle_record[2]}"
        exit_message += f"\nParking Fee: £{parking_charge:.2f}"
        exit_message += f"\n{available_spaces_message}"
        return exit_message
    # Returns exit confirmation message if the status was "exit_success".

    def view_available_parking(self):
        available_spaces = self.model.parking_availability()
        capacity = self.model.capacity
        message = f"\nAvailable Parking Spaces: {available_spaces}/{capacity}"
        return message
    # Retrieves the number of available parking spaces and the capacity to show available parking spaces.

    def query_parking_record(self, ticket_number):
        if not ticket_number.strip():
            return "No ticket number entered. Please your ticket number to query a parking record."
    # Checks to see if a ticket number was entered.
        ticket_number = ticket_number.upper()
        found_record = self.model.find_record_by_ticket(ticket_number)
    # Find the parking record by ticket number.

        if found_record:
            message = "Parking Record Found:"
            message += f"\nTicket Number: {found_record[1]}"
            message += f"\nRegistration Number: {found_record[0]}"
            message += f"\nEntry Time: {found_record[3]}"
            if found_record[4]:
                message += f"\nCar has exited the car park at {found_record[4]}"
                message += f"\nTotal Parking fee: £{found_record[5]}"
            else:
                current_time = datetime.now()
                exit_time = current_time.strftime("%H:%M:%S %Y-%m-%d")
                parking_charge = self.model.parking_fee(found_record[3], exit_time)
                message += f"\nCar is currently parked in parking space {found_record[2]}"
                message += f"\nCurrent cost of parking is: £{parking_charge:.2f}"
            return message
        # Returns messages depending on if the car is currently parked or not.
        else:
            return f"No parking record found for ticket number {ticket_number}. " \
                   f"Please make sure you have correctly entered the ticket number"
        # If no record is found, user is informed.

    def check_file_creation_status(self):
        file_status_created = self.model.data_handler.file_creation_status
        if file_status_created == 'created':
            return "A new CSV file has been created to store the data. You can now start using the car park program."
        return None
    # Retrieves file creation status from DataHandler and returns a message if a new file was created.

    def read_car_parking_data_status(self):
        status = self.model.data_handler.read_car_parking_data()
        if status == "file_not_found":
            return "The CSV file could not be located. Please ensure that the file exists and the file path is correct."
        elif status == "io_error":
            return ("An IO error occurred while reading the file. This could be due to reasons such as file permission "
                    "or a corrupted file.")
        elif status == "csv_error":
            return ("There was an issue while processing the Data file in CSV format. Please review the file contents "
                    "for any formatting issues or invalid data entries.")
        return None
    # Retrieves status of reading data file from DataHandler and returns associated message

    """
    The InterfaceController class extends the BaseController to handle specific user interactions for the car park 
    system within the Model-View-Controller (MVC) architecture. This class acts as an intermediary responsible for 
    interpreting user inputs and invoking the corresponding actions in the Model, ensuring that the View is not directly 
    involved with business logic or data access, thus maintaining a clear separation of concerns.
    """


class InterfaceController(BaseController):
    def __init__(self, model, view):
        super().__init__(model, view)
        self.view = view

    def start_application(self):
        message = self.check_file_creation_status()
        if message:
            self.view.display_message(message)
        message = self.read_car_parking_data_status()
        if message:
            self.view.display_message(message)
    # Checks for file creation status and reads the car parking data at the start.

    def handle_unexpected_error(self, error_message):
        self.view.display_message(f"An unexpected error occurred: {error_message}")
    # Handles unexpected errors and displays error message to user. (Error/Exception handling)

    def handle_return_to_menu(self, input_value):
        return input_value.strip() == "0"
    # This functions allows the user to return to the main menu.

    """
    Last for methods are for handling user interactions. I have taken a modular approach as it allows me to keep the 
    code organised and separate concerns. Each methods also has a try-except blocks to enhance by Error/Exception 
    handling.
    """

    def handle_enter_car_park(self, registration_number):
        try:
            if self.handle_return_to_menu(registration_number):
                return

            status, result = self.car_entry_reg_check(registration_number)
            message = self.car_entry_status(status, result, registration_number)
            if message:
                self.view.display_message(message)
        except Exception as e:
            self.handle_unexpected_error(str(e))

    def handle_exit_car_park(self, registration_exit):
        try:
            if self.handle_return_to_menu(registration_exit):
                return

            exit_message = self.car_exit_status(registration_exit)
            if exit_message:
                self.view.display_message(exit_message)
        except Exception as e:
            self.handle_unexpected_error(str(e))

    def handle_view_parking_spaces(self):
        message = self.view_available_parking()
        self.view.display_message(message)

    def handle_query_parking_record(self, ticket_number):
        try:
            if self.handle_return_to_menu(ticket_number):
                return
            message = self.query_parking_record(ticket_number)
            self.view.display_message(message)
        except Exception as e:
            self.handle_unexpected_error(str(e))
