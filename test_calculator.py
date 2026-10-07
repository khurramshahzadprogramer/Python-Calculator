import unittest
import tkinter as tk
from calculator import CalculatorApp

class TestCalculatorApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        # Hide root window during tests
        self.root.withdraw()
        self.app = CalculatorApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initial_state(self):
        self.assertEqual(self.app.current_input, "0")
        self.assertIsNone(self.app.previous_value)
        self.assertIsNone(self.app.operator)
        self.assertFalse(self.app.error_state)

    def test_addition(self):
        # 5 + 5 = 10
        for char in "5+5=":
            self.app.on_button_click(char)
        self.assertEqual(self.app.current_input, "10")

    def test_subtraction(self):
        # 10 - 4 = 6
        for char in "10-4=":
            self.app.on_button_click(char)
        self.assertEqual(self.app.current_input, "6")

    def test_multiplication(self):
        # 5 * 4 = 20
        for char in "5*4=":
            self.app.on_button_click(char)
        self.assertEqual(self.app.current_input, "20")

    def test_division(self):
        # 20 / 4 = 5
        for char in "20/4=":
            self.app.on_button_click(char)
        self.assertEqual(self.app.current_input, "5")

    def test_decimals(self):
        # 5.5 + 4.2 = 9.7
        for char in "5.5+4.2=":
            self.app.on_button_click(char)
        self.assertEqual(self.app.current_input, "9.7")

    def test_negative_result(self):
        # 3 - 8 = -5
        for char in "3-8=":
            self.app.on_button_click(char)
        self.assertEqual(self.app.current_input, "-5")

    def test_consecutive_calculations(self):
        # 5 + 5 + 10 = 20
        for char in "5+5+10=":
            self.app.on_button_click(char)
        self.assertEqual(self.app.current_input, "20")

    def test_division_by_zero(self):
        # 10 / 0
        for char in "10/0=":
            self.app.on_button_click(char)
        self.assertTrue(self.app.error_state)
        self.assertEqual(self.app.result_label.cget("text"), "Division by zero")

        # Calculator should continue working after 'C' (Clear)
        self.app.on_button_click("C")
        self.assertFalse(self.app.error_state)
        for char in "5+5=":
            self.app.on_button_click(char)
        self.assertEqual(self.app.current_input, "10")

    def test_backspace(self):
        # Type 123, backspace -> 12
        for char in "123":
            self.app.on_button_click(char)
        self.assertEqual(self.app.current_input, "123")
        self.app.backspace()
        self.assertEqual(self.app.current_input, "12")

    def test_clear(self):
        for char in "123+45":
            self.app.on_button_click(char)
        self.app.on_button_click("C")
        self.assertEqual(self.app.current_input, "0")
        self.assertIsNone(self.app.previous_value)
        self.assertIsNone(self.app.operator)

if __name__ == "__main__":
    unittest.main()
