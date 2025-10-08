"""
Unit tests for Bus Boarding Sequence Generator
"""

import unittest
import os
import tempfile
from boarding_sequence import BusBoarding


class TestBusBoarding(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.bus = BusBoarding()
    
    def test_parse_seat(self):
        """Test seat parsing functionality."""
        # Test valid seats
        self.assertEqual(self.bus.parse_seat('A1'), ('A', 1))
        self.assertEqual(self.bus.parse_seat('B20'), ('B', 20))
        self.assertEqual(self.bus.parse_seat('c2'), ('C', 2))
        self.assertEqual(self.bus.parse_seat('D15'), ('D', 15))
        
        # Test invalid seats
        with self.assertRaises(ValueError):
            self.bus.parse_seat('123')
        with self.assertRaises(ValueError):
            self.bus.parse_seat('ABC')
    
    def test_get_seat_distance(self):
        """Test seat distance calculation."""
        self.assertEqual(self.bus.get_seat_distance('A1'), 1)
        self.assertEqual(self.bus.get_seat_distance('A20'), 20)
        self.assertEqual(self.bus.get_seat_distance('C2'), 2)
        self.assertEqual(self.bus.get_seat_distance('B15'), 15)
    
    def test_get_booking_max_distance(self):
        """Test maximum distance calculation for bookings."""
        # Single seat
        self.assertEqual(self.bus.get_booking_max_distance(['A1']), 1)
        
        # Multiple seats - should return max
        self.assertEqual(self.bus.get_booking_max_distance(['A1', 'B1']), 1)
        self.assertEqual(self.bus.get_booking_max_distance(['A20', 'C2']), 20)
        self.assertEqual(self.bus.get_booking_max_distance(['C2', 'A1', 'B15']), 15)
    
    def test_generate_boarding_sequence(self):
        """Test boarding sequence generation."""
        bookings = [
            {'booking_id': 101, 'seats': ['A1', 'B1'], 'max_distance': 1},
            {'booking_id': 120, 'seats': ['A20', 'C2'], 'max_distance': 20},
            {'booking_id': 201, 'seats': ['C2'], 'max_distance': 2},
            {'booking_id': 213, 'seats': ['C18'], 'max_distance': 18}
        ]
        
        result = self.bus.generate_boarding_sequence(bookings)
        
        # Check sequence order (furthest first)
        self.assertEqual(result[0]['booking_id'], 120)  # A20 - furthest
        self.assertEqual(result[1]['booking_id'], 213)  # C18
        self.assertEqual(result[2]['booking_id'], 201)  # C2
        self.assertEqual(result[3]['booking_id'], 101)  # A1 - closest
        
        # Check sequence numbers
        self.assertEqual(result[0]['sequence'], 1)
        self.assertEqual(result[1]['sequence'], 2)
        self.assertEqual(result[2]['sequence'], 3)
        self.assertEqual(result[3]['sequence'], 4)
    
    def test_tie_breaking(self):
        """Test tie-breaking by booking ID."""
        bookings = [
            {'booking_id': 150, 'seats': ['A10'], 'max_distance': 10},
            {'booking_id': 100, 'seats': ['B10'], 'max_distance': 10},
            {'booking_id': 125, 'seats': ['C10'], 'max_distance': 10}
        ]
        
        result = self.bus.generate_boarding_sequence(bookings)
        
        # Same distance, so should be sorted by booking ID
        self.assertEqual(result[0]['booking_id'], 100)
        self.assertEqual(result[1]['booking_id'], 125)
        self.assertEqual(result[2]['booking_id'], 150)
    
    def test_parse_booking_data(self):
        """Test CSV file parsing."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            f.write('Booking_id,Seats\n')
            f.write('101,A1,B1\n')
            f.write('120,A20,C2\n')
            temp_file = f.name
        
        try:
            bookings = self.bus.parse_booking_data(temp_file)
            
            self.assertEqual(len(bookings), 2)
            self.assertEqual(bookings[0]['booking_id'], 101)
            self.assertEqual(bookings[0]['seats'], ['A1', 'B1'])
            self.assertEqual(bookings[1]['booking_id'], 120)
            self.assertEqual(bookings[1]['seats'], ['A20', 'C2'])
        finally:
            os.unlink(temp_file)
    
    def test_display_simple_sequence(self):
        """Test simple output format."""
        bookings = [
            {'booking_id': 120, 'seats': ['A20'], 'sequence': 1, 'max_distance': 20},
            {'booking_id': 101, 'seats': ['A1'], 'sequence': 2, 'max_distance': 1}
        ]
        
        output = self.bus.display_simple_sequence(bookings)
        
        self.assertIn('Seq', output)
        self.assertIn('Booking_ID', output)
        self.assertIn('1', output)
        self.assertIn('120', output)
        self.assertIn('2', output)
        self.assertIn('101', output)
    
    def test_full_workflow(self):
        """Test complete workflow from file to output."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            f.write('Booking_id,Seats\n')
            f.write('101,A1,b1\n')
            f.write('120,A20,c2\n')
            f.write('201,c2\n')
            f.write('213,c18\n')
            temp_file = f.name
        
        try:
            result = self.bus.process_file(temp_file, simple_output=True)
            
            # Verify output contains expected data
            self.assertIn('120', result)  # First in sequence
            self.assertIn('213', result)  # Second
            self.assertIn('201', result)  # Third
            self.assertIn('101', result)  # Fourth (last)
            
            # Verify it's in correct order
            pos_120 = result.index('120')
            pos_213 = result.index('213')
            pos_201 = result.index('201')
            pos_101 = result.index('101')
            
            self.assertLess(pos_120, pos_213)
            self.assertLess(pos_213, pos_201)
            self.assertLess(pos_201, pos_101)
        finally:
            os.unlink(temp_file)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
