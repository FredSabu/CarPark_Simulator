import csv
import time
import random
from datetime import datetime


class BinarySearchTreeNode:
    @staticmethod
    def binary_search(data_list, target, key_function):
        left, right = 0, len(data_list) - 1

        while left <= right:
            mid = (left + right) // 2
            row = data_list[mid]

            if key_function(row) == target:
                return row
            elif key_function(row) < target:
                left = mid + 1
            else:
                right = mid - 1

        return None


class DataHandler:
    def __init__(self, data_file):
        self.data_file = data_file

    def read_car_parking_data(self):
        try:
            with open(self.data_file, "r") as file:
                car_parking_reader = csv.reader(file)
                return list(car_parking_reader)
        except FileNotFoundError:
            print(f"Error: The file {self.data_file} was not found.")
            return []

    def update_car_parking_data(self, car_parking_data):
        with open(self.data_file, "w", newline="") as update_file:
            car_parking_update = csv.writer(update_file)
            for data_row in car_parking_data:
                car_parking_update.writerow(data_row)


class Model:
    def __init__(self, capacity, data_file):
        self.capacity = capacity
        self.data_handler = DataHandler(data_file)
        self.available_spaces = self.parking_availability()

    def read_car_parking_data(self):
        return self.data_handler.read_car_parking_data()

    def update_car_parking_data(self, car_parking_data):
        self.data_handler.update_car_parking_data(car_parking_data)

    def parking_availability(self):
        rows = self.data_handler.read_car_parking_data()
        occupied_spaces = [row for row in rows if not row[4]]
        return self.capacity - len(occupied_spaces)

    def get_occupied_slots(self):
        rows = self.data_handler.read_car_parking_data()  # Use DataHandler
        occupied_slots = set()
        for row in rows:
            if not row[4]:
                occupied_slots.add(int(row[2]))
        return occupied_slots

    def allocate_parking_slot(self, occupied_slots):
        available_slots = set(range(1, self.capacity + 1)) - occupied_slots

        if available_slots:
            slot_number = min(available_slots)
            return slot_number
        else:
            return None

    def parking_fee(self, entry_time, exit_time):
        entry_datetime = datetime.strptime(entry_time, "%H:%M:%S %Y-%m-%d")
        exit_datetime = datetime.strptime(exit_time, "%H:%M:%S %Y-%m-%d")
        time_difference = exit_datetime - entry_datetime
        hours_parked = time_difference.total_seconds() / 3600
        hourly_rate = 2
        total_fee = hours_parked * hourly_rate
        return total_fee

    def update_parking_data(self, registration_number, ticket_number, parking_slot, entry_time):
        car_parking_data = [registration_number, ticket_number, parking_slot, entry_time, None, None]

        car_parking_data_list = self.data_handler.read_car_parking_data()
        car_parking_data_list.append(car_parking_data)

        self.data_handler.update_car_parking_data(car_parking_data_list)

    def is_already_parked(self, registration_number):
        car_parking_data = self.read_car_parking_data()
        for row in car_parking_data:
            if not row[4] and row[0].strip().upper() == registration_number.upper():
                return True
        return False

    def process_car_entry(self, registration_number):
        if self.available_spaces <= 0:
            return "full", None

        occupied_slots = self.get_occupied_slots()
        if self.is_already_parked(registration_number):
            return "already_parked", None

        parking_slot = self.allocate_parking_slot(occupied_slots)
        if parking_slot is not None:
            entry_time = time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())
            ticket_number = registration_number.upper().replace(" ", "") + str(random.randint(1, 99))
            self.available_spaces -= 1
            self.update_parking_data(registration_number, ticket_number, parking_slot, entry_time)
            return "success", (parking_slot, ticket_number)
        else:
            return "full", None

    def process_exit(self, registration_exit, car_parking_data):
        sorted_car_parking_data = sorted(car_parking_data, key=lambda row: row[0].strip())

        def get_registration(row):
            return row[0].strip()

        found_record = BinarySearchTreeNode.binary_search(
            sorted_car_parking_data, registration_exit, get_registration
        )

        if found_record and not found_record[4]:
            entry_time = found_record[3]

            exit_time = time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())
            parking_charge = self.parking_fee(entry_time, exit_time)

            found_record[4] = exit_time
            found_record[5] = "{:.2f}".format(parking_charge)

            self.available_spaces += 1
            return "exit_success", found_record, parking_charge  # Return necessary data
        else:
            return "not_parked", None, None

    def get_available_parking_spaces(self):
        return self.available_spaces, self.capacity

    def find_record_by_ticket(self, ticket_number):
        ticket_search_data = self.read_car_parking_data()
        ticket_search_data.sort(key=lambda row: row[1])

        def get_ticket(row):
            return row[1]

        return BinarySearchTreeNode.binary_search(ticket_search_data, ticket_number, get_ticket)

