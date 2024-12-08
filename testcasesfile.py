
import unittest
from project import Hotel, Room, Booking, Customer
import datetime

class TestHotelBookingSystem(unittest.TestCase):
    def setUp(self):
        self.hotel = Hotel("Grand Stay")
        self.hotel.add_room(101, 'Single')
        self.hotel.add_room(102, 'Double')
        self.hotel.add_room(201, 'Suite')
        self.hotel.add_customer("Alice", "alice@example.com")
        self.hotel.add_customer("Bob", "bob@example.com")

    def test_room_booking(self):
        check_in = datetime.date.today() + datetime.timedelta(days=1)
        check_out = datetime.date.today() + datetime.timedelta(days=3)
        result = self.hotel.book_room("Alice", 'Single', check_in, check_out)
        self.assertIn("booked", result)

    def test_booking_no_available_rooms(self):
        check_in = datetime.date.today() + datetime.timedelta(days=1)
        check_out = datetime.date.today() + datetime.timedelta(days=7)
        self.hotel.book_room("Alice", 'Suite', check_in, check_out)
        result = self.hotel.book_room("Bob", 'Suite', check_in, check_out)
        self.assertIn("No available rooms", result)

    def test_booking_cancellation_successful(self):
        check_in = datetime.date.today() + datetime.timedelta(days=5)
        check_out = datetime.date.today() + datetime.timedelta(days=7)
        self.hotel.book_room("Alice", 'Double', check_in, check_out)
        result = self.hotel.cancel_booking("Alice")
        self.assertIn("Booking canceled", result)

    def test_booking_cancellation_denied(self):
        check_in = datetime.date.today() + datetime.timedelta(days=1)
        check_out = datetime.date.today() + datetime.timedelta(days=4)
        self.hotel.book_room("Alice", 'Single', check_in, check_out)
        result = self.hotel.cancel_booking("Alice")
        self.assertIn("Cancellation denied", result)

    def test_invalid_room_type(self):
        result = self.hotel.add_room(301, 'Penthouse')
        self.assertIn("Invalid room type", result)

    def test_room_availability(self):
        availability = self.hotel.view_room_availability()
        self.assertEqual(len(availability), 3)
        self.assertIn("Room 101", availability[0])

    def test_booking_summary(self):
        check_in = datetime.date.today() + datetime.timedelta(days=1)
        check_out = datetime.date.today() + datetime.timedelta(days=5)
        self.hotel.book_room("Alice", 'Single', check_in, check_out)
        summary = self.hotel.get_booking_summary()
        self.assertEqual(len(summary), 1)
        self.assertIn("Alice", summary[0])

    def test_customer_details(self):
        check_in = datetime.date.today() + datetime.timedelta(days=2)
        check_out = datetime.date.today() + datetime.timedelta(days=4)
        self.hotel.book_room("Alice", 'Single', check_in, check_out)
        details = self.hotel.get_customer_details("Alice")
        self.assertEqual(len(details), 1)
        self.assertIn("Room 101", details[0])

    def test_add_feature_to_room(self):
        room = next(room for room in self.hotel.rooms if room.room_number == 101)
        result = room.add_feature("Ocean View")
        self.assertIn("Feature 'Ocean View'", result)

    def test_customer_not_found(self):
        details = self.hotel.get_customer_details("Charlie")
        self.assertIn("Customer Charlie not found", details)

if __name__ == '__main__':
    unittest.main()