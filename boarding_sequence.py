"""
Bus Boarding Sequence Generator
Generates optimal boarding sequence to maximize boarding time by boarding passengers
with furthest seats first (back to front strategy).
"""

import re
from typing import List, Tuple, Dict


class BusBoarding:
    def __init__(self):
        """Initialize the bus boarding system."""
        pass
    
    def parse_seat(self, seat: str) -> Tuple[str, int]:
        """
        Parse a seat label into row letter and number.
        
        Args:
            seat: Seat label (e.g., 'A1', 'B20', 'C2')
            
        Returns:
            Tuple of (row_letter, seat_number)
        """
        seat = seat.strip().upper()
        match = re.match(r'([A-Z])(\d+)', seat)
        if match:
            row_letter = match.group(1)
            seat_number = int(match.group(2))
            return row_letter, seat_number
        raise ValueError(f"Invalid seat format: {seat}")
    
    def get_seat_distance(self, seat: str) -> int:
        """
        Calculate the distance of a seat from the front entry.
        Higher number = further from entry (e.g., A20 > A1).
        
        Args:
            seat: Seat label (e.g., 'A1', 'B20')
            
        Returns:
            Distance value (seat number)
        """
        _, seat_number = self.parse_seat(seat)
        return seat_number
    
    def get_booking_max_distance(self, seats: List[str]) -> int:
        """
        Get the maximum distance among all seats in a booking.
        For max boarding time, we prioritize bookings with furthest seats.
        
        Args:
            seats: List of seat labels for a booking
            
        Returns:
            Maximum distance value
        """
        return max(self.get_seat_distance(seat) for seat in seats)
    
    def parse_booking_data(self, file_path: str) -> List[Dict]:
        """
        Parse booking data from CSV file.
        
        Args:
            file_path: Path to the booking data file
            
        Returns:
            List of booking dictionaries
        """
        bookings = []
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            # Skip header
            for i in range(1, len(lines)):
                line = lines[i].strip()
                if not line:
                    continue
                
                # Split by comma to get booking_id and seats
                parts = [p.strip() for p in line.split(',')]
                if len(parts) < 2:
                    continue
                
                booking_id = int(parts[0])
                seats = parts[1:]  # All remaining parts are seats
                
                bookings.append({
                    'booking_id': booking_id,
                    'seats': seats,
                    'max_distance': self.get_booking_max_distance(seats)
                })
        
        return bookings
    
    def generate_boarding_sequence(self, bookings: List[Dict]) -> List[Dict]:
        """
        Generate boarding sequence for maximum boarding time.
        Strategy: Board passengers with furthest seats first (back to front).
        
        Args:
            bookings: List of booking dictionaries
            
        Returns:
            Sorted list of bookings with sequence numbers
        """
        # Sort by:
        # 1. Maximum distance (descending) - furthest seats first
        # 2. Booking ID (ascending) - earlier bookings first for tie-breaking
        sorted_bookings = sorted(
            bookings,
            key=lambda x: (-x['max_distance'], x['booking_id'])
        )
        
        # Add sequence numbers
        for seq, booking in enumerate(sorted_bookings, start=1):
            booking['sequence'] = seq
        
        return sorted_bookings
    
    def display_sequence(self, bookings: List[Dict]) -> str:
        """
        Generate UI-friendly output format.
        
        Args:
            bookings: Sorted list of bookings with sequence numbers
            
        Returns:
            Formatted string for display
        """
        output = []
        output.append(f"{'Seq':<6} {'Booking_ID':<12} {'Seats':<20} {'Max_Distance'}")
        output.append("-" * 60)
        
        for booking in bookings:
            seats_str = ','.join(booking['seats'])
            output.append(
                f"{booking['sequence']:<6} {booking['booking_id']:<12} "
                f"{seats_str:<20} {booking['max_distance']}"
            )
        
        return '\n'.join(output)
    
    def display_simple_sequence(self, bookings: List[Dict]) -> str:
        """
        Generate simple UI-friendly output format (Seq and Booking_ID only).
        
        Args:
            bookings: Sorted list of bookings with sequence numbers
            
        Returns:
            Formatted string for display
        """
        output = []
        output.append(f"{'Seq':<6} {'Booking_ID'}")
        output.append("-" * 20)
        
        for booking in bookings:
            output.append(f"{booking['sequence']:<6} {booking['booking_id']}")
        
        return '\n'.join(output)
    
    def process_file(self, input_file: str, output_file: str = None, 
                     simple_output: bool = False) -> str:
        """
        Process booking file and generate boarding sequence.
        
        Args:
            input_file: Path to input CSV file
            output_file: Optional path to save output
            simple_output: If True, show only Seq and Booking_ID
            
        Returns:
            Formatted output string
        """
        # Parse bookings
        bookings = self.parse_booking_data(input_file)
        
        # Generate sequence
        sorted_bookings = self.generate_boarding_sequence(bookings)
        
        # Display results
        if simple_output:
            result = self.display_simple_sequence(sorted_bookings)
        else:
            result = self.display_sequence(sorted_bookings)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(result)
        
        return result


def main():
    """Main function to run the boarding sequence generator."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python boarding_sequence.py <input_file> [output_file] [--simple]")
        print("\nExample: python boarding_sequence.py bookings.csv output.txt --simple")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    simple_output = '--simple' in sys.argv
    
    # Create boarding system
    bus = BusBoarding()
    
    try:
        # Process file
        result = bus.process_file(input_file, output_file, simple_output)
        print(result)
        
        if output_file:
            print(f"\n✓ Output saved to: {output_file}")
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
