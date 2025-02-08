# Calculator Resource IDs

## Layout Resource IDs

### Main Layout
```
calculator_layout      - Main layout container
```

### Display Elements
```
expression_display    - TextView for ongoing expression
calculator_display    - TextView for current number/result
```

### Number Buttons
```
btn_zero             - Button "0"
btn_one              - Button "1"
btn_two              - Button "2"
btn_three            - Button "3"
btn_four             - Button "4"
btn_five             - Button "5"
btn_six              - Button "6"
btn_seven            - Button "7"
btn_eight            - Button "8"
btn_nine             - Button "9"
```

### Operator Buttons
```
btn_add              - Addition operator "+"
btn_subtract         - Subtraction operator "-"
btn_multiply         - Multiplication operator "×"
btn_divide           - Division operator "÷"
```

### Function Buttons
```
btn_equals           - Equals button "="
btn_clear            - Clear button "C"
btn_decimal          - Decimal point button "."
btn_backspace        - Backspace button "⌫"
btn_percent          - Percentage button "%"
```

## Testing Examples

### Appium Example
```java
// Find elements using resource IDs
driver.findElement(By.id("com.zilogic.z_calc:id/btn_one"));
driver.findElement(By.id("com.zilogic.z_calc:id/btn_add"));
driver.findElement(By.id("com.zilogic.z_calc:id/calculator_display"));
```

## Content Descriptions
All buttons have content descriptions for accessibility testing:
```
Number 0-9           - "Number X"
Add Button           - "Add Button"
Subtract Button      - "Subtract Button"
Multiply Button      - "Multiply Button"
Divide Button        - "Divide Button"
Clear Button         - "Clear Button"
Equals Button        - "Equals Button"
Decimal Point        - "Decimal Point"
Backspace Button     - "Backspace Button"
Percent Button       - "Percent Button"
Expression Display   - "Expression Display"
Result Display       - "Result Display"
```

## Layout Hierarchy
```
LinearLayout (calculator_layout)
├── LinearLayout
│   ├── TextView (expression_display)
│   └── TextView (calculator_display)
└── GridLayout (calculator_grid)
    ├── Button (btn_clear)
    ├── Button (btn_backspace)
    ├── Button (btn_percent)
    ├── Button (btn_divide)
    ├── Button (btn_seven)
    ├── Button (btn_eight)
    ├── Button (btn_nine)
    ├── Button (btn_multiply)
    ├── Button (btn_four)
    ├── Button (btn_five)
    ├── Button (btn_six)
    ├── Button (btn_subtract)
    ├── Button (btn_one)
    ├── Button (btn_two)
    ├── Button (btn_three)
    ├── Button (btn_add)
    ├── Button (btn_zero)
    ├── Button (btn_decimal)
    └── Button (btn_equals)
```

This comprehensive list of resource IDs can be used for:
1. UI Automation Testing
2. Accessibility Testing
3. Layout Testing
4. Integration Testing

The IDs follow a consistent naming convention:
- btn_* for buttons
- *_display for display elements
- calculator_* for main layout elements