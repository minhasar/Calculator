# Python Calculator - AI Assistant Guidelines

## Project Overview
A command-line Python calculator supporting basic arithmetic operations (add, subtract, multiply, divide) with comprehensive unit tests.

## Quick Start

### Running the Calculator
```bash
python calculator.py
```

### Running Tests (requires pytest)
```bash
pytest tests/ -v
```

## Project Structure

- **calculator.py** - Core module with arithmetic functions and interactive CLI
- **tests/test_calculator.py** - Comprehensive unit tests using pytest
- **README.md** - User documentation
- **.github/copilot-instructions.md** - This file

## Architecture & Key Patterns

### Function Design (calculator.py)
- **Type-hinted functions**: All arithmetic functions include parameter and return type hints
  - `add(a: float, b: float) -> float`
  - `divide(a: float, b: float) -> float` (includes zero-check)
- **Docstrings**: Every function has a concise docstring describing its purpose
- **Error handling**: `divide()` raises `ValueError` for division by zero
- **Interactive CLI**: `main()` loop provides user-friendly interface with input validation

### Testing Strategy (tests/test_calculator.py)
- **Pytest framework**: Organize tests using test classes (TestAdd, TestSubtract, etc.)
- **Coverage**: Test positive/negative numbers, zero cases, and error conditions
- **Exception testing**: Use `pytest.raises()` for error cases (e.g., divide by zero)

## Development Conventions

1. **Type Hints**: Always add type hints to function parameters and returns
2. **Docstrings**: Use single-line docstrings for simple functions
3. **Error Handling**: Validate input in the CLI loop; let functions handle logical errors
4. **Testing**: Add tests alongside features; maintain test class organization
5. **Input Validation**: Parse user expressions defensively (check format, operator validity)

## Adding New Features

### New Arithmetic Operation
1. Add function to `calculator.py` with type hints and docstring
2. Create test class in `tests/test_calculator.py` covering edge cases
3. Update `main()` to handle the new operator
4. Update README.md with the new operation

### Example: Adding Power Function
```python
def power(a: float, b: float) -> float:
    """Raise a to the power of b."""
    return a ** b
```

Then add tests and CLI support.

## Common Commands

```bash
# Run specific test class
pytest tests/test_calculator.py::TestDivide -v

# Run with coverage (requires pytest-cov)
pytest --cov=. tests/

# Run calculator and test an expression
python calculator.py
```

## Key Files to Know

- `calculator.py` (lines 1-28): Function definitions with type hints
- `calculator.py` (lines 31-67): Interactive main loop with input parsing
- `tests/test_calculator.py`: Test organization by arithmetic operation

## Notes for AI Assistants

- The project prioritizes clarity and testability over complexity
- All user-facing messages are in the `main()` function
- Mathematical operations are isolated in simple, pure functions
- Tests follow a consistent class-based organization by operation
