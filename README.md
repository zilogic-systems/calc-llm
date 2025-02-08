# Android Calculator App for LLM Demo

A basic calculator application developed in Kotlin with intentionally implemented bugs for llm-demo. This application serves as a testing ground for various scenarios including exception handling, input validation, and arithmetic operations.

## Features

- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Percentage calculations
- Decimal point support
- Backspace functionality
- Ongoing expression display
- Clear function
- Edge-to-edge display support

## Setup

1. Clone the repository
2. Open the project in Android Studio
3. Sync Gradle files
4. Run on an emulator or physical device

## Project Structure

```
app/
├── src/
│   ├── main/
│   │   ├── java/com/zilogic/z_calc/
│   │   │   └── MainActivity.kt
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   └── activity_main.xml
│   │   │   └── values/
│   │   │       └── dimens.xml
│   │   └── AndroidManifest.xml
│   └── test/
└── build.gradle
```

## Intentional Bugs for Testing

### 1. Consecutive Operations Bug
- **Description**: Application throws exception after 5 consecutive operations
- **Location**: `processOperator()` function
- **Test Steps**:
    1. Enter a number (e.g., 5)
    2. Press any operator (+, -, ×, ÷)
    3. Repeat 5 times
- **Expected Result**: RuntimeException after 5 consecutive operations

### 2. Number Length Bug
- **Description**: Input limited to 8 digits
- **Location**: `processNumber()` function
- **Test Steps**:
    1. Try entering a 9-digit number
- **Expected Result**: Toast message warning at 8 digits

### 3. Large Number Multiplication Bug
- **Description**: Exception thrown for numbers > 999,999
- **Location**: `processEquals()` function
- **Test Steps**:
    1. Enter 1000000
    2. Press × (multiply)
    3. Enter 2
    4. Press =
- **Expected Result**: ArithmeticException for large numbers

### 4. Division by Zero Bug
- **Description**: Throws arithmetic exception
- **Location**: `processEquals()` function
- **Test Steps**:
    1. Enter any number
    2. Press ÷ (divide)
    3. Enter 0
    4. Press =
- **Expected Result**: ArithmeticException "Division by zero!"

### 5. Multiple Decimal Points Bug
- **Description**: Allows multiple decimal points in a number
- **Location**: `processDecimal()` function
- **Test Steps**:
    1. Enter 1.2.3
- **Expected Result**: Invalid number with multiple decimal points accepted

### 6. Silent Failure Bug
- **Description**: No error message for invalid number format
- **Location**: catch block in `processPercent()`
- **Test Steps**:
    1. Create invalid number format scenario
- **Expected Result**: Operation fails silently without user notification

### 7. Percentage Calculation Bug
- **Description**: Incorrect percentage calculation
- **Location**: `processPercent()` function
- **Test Steps**:
    1. Enter a number
    2. Press % button
- **Expected Result**: Incorrect percentage result (divides by 100 without context)

### 8. Number Format Bug
- **Description**: No handling of infinity or NaN values
- **Location**: `formatResult()` function
- **Test Steps**:
    1. Perform operations resulting in infinity
    2. Create NaN scenarios
- **Expected Result**: Improper handling of special numeric values

## Test Coverage Areas

1. Input Validation
    - Number length limits
    - Decimal point handling
    - Invalid input scenarios

2. Arithmetic Operations
    - Basic calculations
    - Large number operations
    - Division by zero
    - Percentage calculations

3. State Management
    - Expression building
    - Result display
    - Operation chaining

4. Error Handling
    - Exception scenarios
    - User notifications
    - Recovery from errors

## Testing Resources

For UI automation testing purposes, refer to [resource-id.md](resource-id.md) which contains:

- Complete list of all resource IDs
- Layout hierarchy
- Content descriptions
- Testing examples for Appium

## License

This project is licensed under the Apache License, Version 2.0 (the "License");