#Hotel room booking
import datetime

# Constants
ROOM_TYPES = {
    'Single': {'rate': 100, 'capacity': 1},
    'Double': {'rate': 150, 'capacity': 2},
    'Suite': {'rate': 300, 'capacity': 4}
}
MIN_DAYS_BEFORE_CANCELLATION = 2
TAX_RATE = 0.1

# Room class
class Room:
    def __init__(self, room_number, room_type):
        self.room_number = room_number
        self.room_type = room_type
        self.rate = ROOM_TYPES[room_type]['rate']
        self.is_booked = False
        self.features = []

    def add_feature(self, feature):
        self.features.append(feature)
        return f"Feature '{feature}' added to Room {self.room_number}"

    def book(self):
        if self.is_booked:
            return f"Room {self.room_number} is already booked."
        self.is_booked = True
        return f"Room {self.room_number} booked successfully."

    def cancel_booking(self):
        if not self.is_booked:
            return f"Room {self.room_number} is not currently booked."
        self.is_booked = False
        return f"Booking for room {self.room_number} has been canceled."

# Customer class
class Customer:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info
        self.bookings = []

    def add_booking(self, booking):
        self.bookings.append(booking)

# Booking class
class Booking:
    def __init__(self, customer, room, check_in_date, check_out_date):
        self.customer = customer
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.booked_on = datetime.datetime.now()
        self.is_active = True
        self.total_cost = self.calculate_cost()

    def calculate_cost(self):
        nights = (self.check_out_date - self.check_in_date).days
        base_cost = nights * self.room.rate
        tax = base_cost * TAX_RATE
        return base_cost + tax

    def cancel(self):
        if not self.is_active:
            return "Booking is already canceled."
        self.room.cancel_booking()
        self.is_active = False
        return "Booking canceled successfully."

# Hotel class
class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.customers = []
        self.bookings = []

    def add_room(self, room_number, room_type):
        if room_type not in ROOM_TYPES:
            return "Invalid room type."
        room = Room(room_number, room_type)
        self.rooms.append(room)
        return f"Room {room_number} added as a {room_type}."

    def add_customer(self, name, contact_info):
        customer = Customer(name, contact_info)
        self.customers.append(customer)
        return f"Customer {name} added."

    def view_room_availability(self):
        available_rooms = [f"Room {room.room_number} ({', '.join(room.features)}): {room.room_type}" for room in self.rooms if not room.is_booked]
        return available_rooms if available_rooms else ["No rooms available."]

    def find_available_room(self, room_type):
        for room in self.rooms:
            if room.room_type == room_type and not room.is_booked:
                return room
        return None

    def book_room(self, customer_name, room_type, check_in_date, check_out_date):
        room = self.find_available_room(room_type)
        if not room:
            return "No available rooms of this type."

        customer = next((c for c in self.customers if c.name == customer_name), None)
        if not customer:
            return f"Customer {customer_name} not found."

        room.book()
        booking = Booking(customer, room, check_in_date, check_out_date)
        self.bookings.append(booking)
        customer.add_booking(booking)
        return f"Room {room.room_number} booked for {customer_name} from {check_in_date} to {check_out_date}. Total Cost: {booking.total_cost}"

    def cancel_booking(self, customer_name):
        for booking in self.bookings:
            if booking.customer.name == customer_name and booking.is_active:
                cancellation_notice_period = (booking.check_in_date - datetime.datetime.now().date()).days
                if cancellation_notice_period < MIN_DAYS_BEFORE_CANCELLATION:
                    return "Cancellation denied. Insufficient notice."
                return booking.cancel()
        return "Active booking not found for cancellation."

    def get_booking_summary(self):
        summary = []
        for booking in self.bookings:
            if booking.is_active:
                summary.append(
                    f"Booking for {booking.customer.name}: Room {booking.room.room_number} "
                    f"from {booking.check_in_date} to {booking.check_out_date}, Cost: {booking.total_cost}"
                )
        return summary

    def get_customer_details(self, name):
        customer = next((c for c in self.customers if c.name == name), None)
        if not customer:
            return f"Customer {name} not found."
        bookings = [f"Room {b.room.room_number}, Check-in: {b.check_in_date}, Check-out: {b.check_out_date}" for b in customer.bookings if b.is_active]
        return bookings if bookings else ["No active bookings found for this customer."]

def exit_program():
    print("Exiting the system.")
    quit()

def main():
    hotel = Hotel("Grand Stay")
    
    hotel.add_room(101, 'Single')
    hotel.add_room(102, 'Double')
    hotel.add_room(201, 'Suite')
    hotel.add_room(301, 'Single')
    hotel.add_room(302, 'Double')

    hotel.add_customer("Alice", "alice@example.com")
    hotel.add_customer("Bob", "bob@example.com")

    while True:
        print("\n=== Hotel Booking System ===")
        print("1. Book a Room")
        print("2. Cancel a Booking")
        print("3. View Booking Summary")
        print("4. View Room Availability")
        print("5. View Customer Details")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer_name = input("Enter customer name: ")
            room_type = input(f"Enter room type ({', '.join(ROOM_TYPES.keys())}): ")
            check_in = datetime.datetime.strptime(
                input("Enter check-in date (YYYY-MM-DD): "), "%Y-%m-%d"
            ).date()
            check_out = datetime.datetime.strptime(
                input("Enter check-out date (YYYY-MM-DD): "), "%Y-%m-%d"
            ).date()
            print(hotel.book_room(customer_name, room_type, check_in, check_out))
        
        elif choice == "2":
            customer_name = input("Enter customer name to cancel booking: ")
            print(hotel.cancel_booking(customer_name))

        elif choice == "3":
            summary = hotel.get_booking_summary()
            if not summary:
                print("No active bookings found.")
            else:
                for line in summary:
                    print(line)

        elif choice == "4":
            availability = hotel.view_room_availability()
            for room in availability:
                print(room)

        elif choice == "5":
            customer_name = input("Enter customer name: ")
            details = hotel.get_customer_details(customer_name)
            for detail in details:
                print(detail)

        elif choice == "6":
            exit_program()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
