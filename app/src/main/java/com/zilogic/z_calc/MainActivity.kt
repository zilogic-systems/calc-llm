package com.zilogic.z_calc

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.zilogic.z_calc.databinding.ActivityMainBinding

/**
 * Calculator application with intentional bugs for testing purposes.
 *
 * Intentional Bugs List:
 * 1. Consecutive Operations Bug:
 *    - Throws exception after 5 consecutive operations
 *    - Location: processOperator() function
 *    - Test: Perform more than 5 operations consecutively
 *
 * 2. Number Length Bug:
 *    - Limits input to 8 digits with error toast
 *    - Location: processNumber() function
 *    - Test: Try to enter a 9-digit number
 *
 * 3. Large Number Multiplication Bug:
 *    - Throws exception for numbers > 999,999 in multiplication
 *    - Location: processEquals() function
 *    - Test: Multiply 1000000 × 2
 *
 * 4. Division by Zero Bug:
 *    - Throws arithmetic exception
 *    - Location: processEquals() function
 *    - Test: Divide any number by 0
 *
 * 5. Multiple Decimal Points Bug:
 *    - Allows multiple decimal points in a number
 *    - Location: processDecimal() function
 *    - Test: Enter number like 1.2.3
 *
 * 6. Silent Failure Bug:
 *    - Silent failure on invalid number format
 *    - Location: catch block in processPercent()
 *    - Test: Operations with invalid number formats
 *
 * 7. Percentage Calculation Bug:
 *    - Incorrect percentage calculation
 *    - Location: processPercent() function
 *    - Test: Calculate percentages of numbers
 *
 * 8. Number Format Bug:
 *    - No handling of infinity or NaN values
 *    - Location: formatResult() function
 *    - Test: Operations resulting in infinity or NaN
 */
class MainActivity : AppCompatActivity() {
    private data class CalculatorState(
        val currentNumber: String = "",
        val operator: String = "",
        val firstNumber: Double = 0.0,
        val isNewNumber: Boolean = true,
        val consecutiveOperations: Int = 0,
        val expression: String = ""
    )

    private sealed class CalculatorAction {
        data class Number(val value: Int) : CalculatorAction()
        data class Operator(val value: String) : CalculatorAction()
        object Equals : CalculatorAction()
        object Clear : CalculatorAction()
        object Decimal : CalculatorAction()
        object Backspace : CalculatorAction()
        object Percent : CalculatorAction()
    }

    private val binding by lazy { ActivityMainBinding.inflate(layoutInflater) }
    private val initialState = CalculatorState()
    private val maxConsecutiveOperations = 5
    private var currentState = CalculatorState()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(binding.root)

        setupEdgeToEdge()
        setupButtons()
        updateDisplays("0")
    }

    private fun setupEdgeToEdge() {
        ViewCompat.setOnApplyWindowInsetsListener(binding.calculatorLayout) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    private fun setupButtons() {
        with(binding) {
            val numberButtons = mapOf(
                btnZero to 0, btnOne to 1, btnTwo to 2, btnThree to 3,
                btnFour to 4, btnFive to 5, btnSix to 6, btnSeven to 7,
                btnEight to 8, btnNine to 9
            )

            numberButtons.forEach { (button, number) ->
                button.setOnClickListener {
                    currentState = processAction(CalculatorAction.Number(number), currentState)
                }
            }

            mapOf(
                btnAdd to "+",
                btnSubtract to "-",
                btnMultiply to "×",
                btnDivide to "÷"
            ).forEach { (button, op) ->
                button.setOnClickListener {
                    currentState = processAction(CalculatorAction.Operator(op), currentState)
                }
            }

            btnEquals.setOnClickListener {
                currentState = processAction(CalculatorAction.Equals, currentState)
            }
            btnClear.setOnClickListener {
                currentState = processAction(CalculatorAction.Clear, currentState)
            }
            btnDecimal.setOnClickListener {
                currentState = processAction(CalculatorAction.Decimal, currentState)
            }
            btnBackspace.setOnClickListener {
                currentState = processAction(CalculatorAction.Backspace, currentState)
            }
            btnPercent.setOnClickListener {
                currentState = processAction(CalculatorAction.Percent, currentState)
            }
        }
    }

    private fun processAction(action: CalculatorAction, state: CalculatorState): CalculatorState {
        return when (action) {
            is CalculatorAction.Number -> processNumber(action.value, state)
            is CalculatorAction.Operator -> processOperator(action.value, state)
            is CalculatorAction.Equals -> processEquals(state)
            is CalculatorAction.Clear -> initialState.also {
                updateDisplays("0")
                binding.expressionDisplay.visibility = View.GONE
            }

            is CalculatorAction.Decimal -> processDecimal(state)
            is CalculatorAction.Backspace -> processBackspace(state)
            is CalculatorAction.Percent -> processPercent(state)
        }
    }

    private fun processNumber(number: Int, state: CalculatorState): CalculatorState {
        // Bug 2: Number length limitation
        if (state.currentNumber.length >= 8) {
            Toast.makeText(this, "Number too long!", Toast.LENGTH_SHORT).show()
            return state
        }

        val newNumber = if (state.isNewNumber) number.toString() else state.currentNumber + number
        val newExpression = if (state.operator.isEmpty()) {
            newNumber
        } else {
            "${state.expression}$number"
        }

        updateDisplays(newNumber, newExpression)
        binding.expressionDisplay.visibility = View.VISIBLE

        return state.copy(
            currentNumber = newNumber,
            isNewNumber = false,
            expression = newExpression
        )
    }

    private fun processOperator(newOperator: String, state: CalculatorState): CalculatorState {
        // Bug 1: Consecutive operations limit
        if (state.consecutiveOperations >= maxConsecutiveOperations) {
            throw RuntimeException("Too many consecutive operations!")
        }

        return if (state.currentNumber.isNotEmpty()) {
            val newState = if (state.operator.isNotEmpty()) {
                processEquals(state)
            } else state

            val newExpression = "${state.expression}$newOperator"
            updateDisplays(newState.currentNumber, newExpression)
            binding.expressionDisplay.visibility = View.VISIBLE

            newState.copy(
                firstNumber = newState.currentNumber.toDouble(),
                operator = newOperator,
                isNewNumber = true,
                consecutiveOperations = state.consecutiveOperations + 1,
                expression = newExpression
            )
        } else state
    }

    private fun processEquals(state: CalculatorState): CalculatorState {
        if (state.currentNumber.isEmpty() || state.operator.isEmpty()) return state

        val secondNumber = state.currentNumber.toDouble()
        return try {
            val result = when (state.operator) {
                "+" -> state.firstNumber + secondNumber
                "-" -> state.firstNumber - secondNumber
                "×" -> {
                    // Bug 3: Large multiplication limitation
                    if (state.firstNumber > 999999 || secondNumber > 999999) {
                        throw ArithmeticException("Numbers too large for multiplication!")
                    }
                    state.firstNumber * secondNumber
                }

                "÷" -> {
                    // Bug 4: Division by zero
                    if (secondNumber == 0.0) {
                        throw ArithmeticException("Division by zero!")
                    }
                    state.firstNumber / secondNumber
                }

                else -> 0.0
            }

            val formattedResult = formatResult(result)
            updateDisplays(formattedResult, state.expression)

            state.copy(
                currentNumber = formattedResult,
                operator = "",
                isNewNumber = true,
                consecutiveOperations = 0,
                expression = state.expression
            )
        } catch (e: ArithmeticException) {
            Toast.makeText(this, e.message, Toast.LENGTH_SHORT).show()
            updateDisplays("Error")
            binding.expressionDisplay.visibility = View.GONE
            initialState
        }
    }

    private fun processDecimal(state: CalculatorState): CalculatorState {
        // Bug 5: Multiple decimal points
        val newNumber = if (state.isNewNumber) "0." else state.currentNumber + "."
        val newExpression = if (state.operator.isEmpty()) {
            newNumber
        } else {
            "${state.expression}."
        }

        updateDisplays(newNumber, newExpression)
        binding.expressionDisplay.visibility = View.VISIBLE
        return state.copy(
            currentNumber = newNumber,
            isNewNumber = false,
            expression = newExpression
        )
    }

    private fun processBackspace(state: CalculatorState): CalculatorState {
        if (state.currentNumber.isEmpty() || state.currentNumber == "0") return state

        val newNumber = state.currentNumber.dropLast(1).ifEmpty { "0" }
        val newExpression = state.expression.dropLast(1).ifEmpty { newNumber }

        updateDisplays(newNumber, newExpression)
        return state.copy(
            currentNumber = newNumber,
            expression = newExpression
        )
    }

    private fun processPercent(state: CalculatorState): CalculatorState {
        return if (state.currentNumber.isNotEmpty()) {
            try {
                val number = state.currentNumber.toDouble()
                // Bug 7: Incorrect percentage calculation
                val result = formatResult(number / 100)
                val newExpression = if (state.operator.isEmpty()) {
                    result
                } else {
                    "${state.expression}$result"
                }

                updateDisplays(result, newExpression)
                state.copy(
                    currentNumber = result,
                    expression = newExpression
                )
            } catch (e: NumberFormatException) {
                // Bug 6: Silent failure on invalid number format
                state
            }
        } else state
    }

    private fun updateDisplays(result: String, expression: String = "") {
        binding.calculatorDisplay.text = result
        if (expression.isNotEmpty()) {
            binding.expressionDisplay.text = expression
        }
    }

    private fun formatResult(result: Double): String {
        // Bug 8: No handling of infinity or NaN
        return if (result == result.toLong().toDouble()) {
            result.toLong().toString()
        } else {
            result.toString()
        }
    }
}