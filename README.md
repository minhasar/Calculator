# Python Calculator

A simple command-line calculator application supporting basic arithmetic operations.

## Features

- **Addition** (+)
- **Subtraction** (-)
- **Multiplication** (*)
- **Division** (/) with zero-division protection

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - Or on Windows, use: `python` (and follow Microsoft Store installation)

2. **Install test dependencies** (optional):
   ```bash
   pip install pytest
   ```

## Usage

### Running the Calculator

```bash
python calculator.py
```

### Running the GUI

```bash
python gui.py
```

The GUI provides buttons for digits and operators and an entry field for the expression. Press `=` to evaluate, or `C` to clear.

Example session:
```
=== Python Calculator ===
Operations: +, -, *, /
Type 'quit' to exit

Enter expression (e.g., 5 + 3): 10 + 5
Result: 15

Enter expression (e.g., 5 + 3): 20 / 4
Result: 5.0

Enter expression (e.g., 5 + 3): quit
Goodbye!
```

### Running Tests

```bash
pytest tests/
```

Or with verbose output:
```bash
pytest -v tests/
```

## Project Structure

```
.
├── calculator.py      # Main calculator module
├── gui.py             # Simple Tkinter GUI for the calculator
├── tests/
│   └── test_calculator.py  # Unit tests
├── README.md           # This file
└── .github/
    └── copilot-instructions.md  # AI assistant guidelines
```

## Development

### Adding New Operations

1. Create a new function in `calculator.py` with type hints and docstring
2. Add corresponding tests in `tests/test_calculator.py`
3. Update the `main()` function to handle the new operation

### Running Tests

```bash
pytest tests/ -v
```

## Notes

- All operations work with floating-point numbers
- Division by zero raises a `ValueError`
- Input format: `number operator number` (e.g., `5 + 3`)

## License

MIT
