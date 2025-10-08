<<<<<<< HEAD
# 🚌 Bus Boarding Sequence Generator

A system that generates optimal booking-wise boarding sequences for bus passengers to **maximize boarding time** using a back-to-front strategy with single front entry.

## 📋 Problem Statement

Design and implement a system that:
- Generates a booking-wise boarding sequence for bus passengers
- Uses a single front entry point
- Maximizes boarding time by boarding passengers with furthest seats first
- Produces UI-friendly output showing the boarding order

## 🎯 Strategy

**Max Boarding Time Approach:**
- Passengers seated furthest from the entry (e.g., A20, B20) board **first**
- Passengers seated closest to the entry (e.g., A1, B1) board **last**
- This prevents passengers from blocking the aisle while others try to reach back seats
- In case of ties (same max distance), earlier booking IDs get priority

## 🚌 Bus Layout

```
╔═══════════════════════════╗
║      BACK OF BUS          ║
║   A20/B20    C20/D20      ║
║   A19/B19    C19/D19      ║
║      ...        ...       ║
║   A2/B2      C2/D2        ║
║   A1/B1      C1/D1        ║
║                           ║
║   ↓ FRONT ENTRY ↓         ║
╚═══════════════════════════╝
```

**Entry:** Single front entry point  
**Boarding Direction:** Back to front (A20 → A1)

## 📥 Input Format

CSV file with the following structure:

```csv
Booking_id,Seats
101,A1,b1
120,A20,c2
201,c2
213,c18
```

**Columns:**
- `Booking_id`: Unique booking identifier (integer)
- `Seats`: Comma-separated list of seat labels (e.g., A1, B20, C2)

**Seat Format:**
- Row letter (A, B, C, D) + seat number (1-20)
- Case-insensitive (A1 = a1)
- Higher numbers = further from entry

## 📤 Output Format

### Simple Format (UI-Friendly)
```
Seq    Booking_ID
--------------------
1      120
2      213
3      201
4      101
```

### Detailed Format
```
Seq    Booking_ID   Seats                Max_Distance
------------------------------------------------------------
1      120          A20,c2               20
2      213          c18                  18
3      201          c2                   2
4      101          A1,b1                1
```

## 🚀 Usage

### Python Script

**Basic usage:**
```bash
python boarding_sequence.py sample_bookings.csv
```

**Simple output (Seq + Booking_ID only):**
```bash
python boarding_sequence.py sample_bookings.csv --simple
```

**Save to file:**
```bash
python boarding_sequence.py sample_bookings.csv output.txt --simple
```

### Web UI

1. Open `web_ui.html` in a web browser
2. Enter or paste booking data in CSV format
3. Click "Generate Sequence"
4. View the boarding sequence in an interactive table

**Features:**
- ✨ Beautiful, modern UI with gradient design
- 📊 Interactive table display
- 🔄 Real-time sequence generation
- 📋 Sample data preloaded
- 🚌 Visual bus layout reference

## 🧪 Testing

Run the test suite:

```bash
python test_boarding.py
```

**Test Coverage:**
- Seat parsing and validation
- Distance calculation
- Booking sequence generation
- Tie-breaking logic
- CSV file parsing
- Output formatting
- Complete workflow integration

## 📁 Project Structure

```
bus boarding/
├── boarding_sequence.py    # Core Python implementation
├── web_ui.html             # Interactive web interface
├── sample_bookings.csv     # Sample input data
├── test_boarding.py        # Unit tests
└── README.md               # Documentation
```

## 🔧 Algorithm Details

### 1. Seat Distance Calculation
```python
distance = seat_number  # A20 = 20, A1 = 1
```

### 2. Booking Max Distance
```python
max_distance = max(distance for all seats in booking)
# Booking with A20,C2 → max_distance = 20
```

### 3. Sorting Logic
```python
Sort by:
1. max_distance (descending)  # Furthest first
2. booking_id (ascending)     # Tie-breaker
```

### 4. Example

**Input:**
```
101: A1,B1   → max_distance = 1
120: A20,C2  → max_distance = 20
201: C2      → max_distance = 2
213: C18     → max_distance = 18
```

**Sorting:**
1. 120 (distance=20) - furthest
2. 213 (distance=18)
3. 201 (distance=2)
4. 101 (distance=1) - closest

**Output Sequence:** 120 → 213 → 201 → 101

## ✅ Requirements Fulfilled

- ✅ Single front entry point
- ✅ Max boarding time strategy (back-to-front)
- ✅ Booking-wise sequence generation
- ✅ Multiple seats per booking support
- ✅ Tie-breaking by booking ID
- ✅ UI-friendly output format
- ✅ CSV input parsing
- ✅ Web-based interactive UI
- ✅ Comprehensive testing
- ✅ Complete documentation

## 🎨 Web UI Features

- **Responsive Design:** Works on desktop and mobile
- **Modern Styling:** Gradient backgrounds, smooth animations
- **Interactive Table:** Hover effects, color-coded badges
- **Error Handling:** Clear error messages for invalid input
- **Sample Data:** Pre-loaded example for quick testing
- **Bus Layout:** Visual reference diagram
- **Info Box:** Strategy explanation and usage guide

## 📊 Sample Output

For the provided sample data:

```
Seq    Booking_ID
--------------------
1      120         (A20,C2 - max distance 20)
2      213         (C18 - distance 18)
3      201         (C2 - distance 2)
4      101         (A1,B1 - max distance 1)
```

**Boarding Order Explanation:**
1. **Booking 120** boards first (has A20 - furthest seat)
2. **Booking 213** boards second (has C18)
3. **Booking 201** boards third (has C2)
4. **Booking 101** boards last (has A1,B1 - closest seats)

This ensures passengers don't block the aisle while others try to reach back seats, maximizing overall boarding efficiency.

## 🔍 Edge Cases Handled

- Case-insensitive seat labels (A1 = a1)
- Multiple seats per booking
- Tie-breaking when bookings have same max distance
- Empty lines in CSV
- Invalid seat formats
- Missing files

## 📝 Notes

- The system assumes seat numbers indicate distance from entry (higher = further)
- All passengers board from the front entry
- The strategy prioritizes minimizing aisle blocking
- Bookings are kept together (all passengers in a booking board at the same time)

## 🚀 Quick Start

1. **Prepare your booking data** in CSV format
2. **Run the Python script** or **open the web UI**
3. **Get the boarding sequence** instantly
4. **Use the output** to organize passenger boarding

---

**Built for optimal bus boarding efficiency! 🚌✨**
=======
# Bus-Boarding-Sequence-Generator
>>>>>>> 168e7b7132ffa56634db0caef12b8b6c938f1dc1
