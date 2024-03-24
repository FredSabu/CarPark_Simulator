
---

# Simple Car Park Simulator for System Design and Programming

![image](https://github.com/FredSabu/CarPark_Simulator/assets/130511381/b98fbcbe-75a1-4c7a-94e7-76c22b8f1607)

![image](https://github.com/FredSabu/CarPark_Simulator/assets/130511381/2006b2fd-aebf-4f82-8a66-8598aee3b608)

## Overview

This Car Park Simulator is designed to emulate the operations of a real-world car park management system. It is divided into two parts: a text-based simulation for console use and a GUI-based simulation for enhanced interaction. 

Awarded a final grade of 95/100.

## Features

### Part 1: Text-Based Simulation
- **Initialisation:** Reads initial parking records from a CSV file.
- **Tracking Availability:** Monitors the number and identifiers of available parking spaces.
- **User Interaction:** Provides a menu-driven console interface to enter or exit the car park, view available spaces, and query parking records by ticket number.
- **Parking Assignment:** Allocates parking spaces and issues ticket numbers upon vehicle entry.
- **Fee Processing:** Calculates parking fees upon exit based on time spent.
- **Record Saving:** Updates and saves parking records to a CSV file when exiting the program.

### Part 2: GUI-Based Simulation
- **Graphical Interface:** A TKinter-based GUI that replicates the console program's features for improved user interaction.
- **Interactive Menus:** Simplifies navigation within the program through clickable buttons and menus.
- **Real-Time Updates:** Displays available parking spaces dynamically.
- **Transaction Logging:** Maintains records of vehicle entry and exit along with timestamps.
- **Fee Calculation:** Computes parking fees at £2 per hour.
- **Ticket Lookup:** Enables searching for parking records using the ticket number.

## User Input Validation

Robust input validation and error handling are integral to this program, ensuring inputs are accurate and the user experience is seamless. The program is designed to maintain data consistency, automatically updating the parking records upon closure to reflect the latest state for subsequent sessions.

---



