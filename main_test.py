import unittest
from main import calculate_average, get_student_average, get_top_student, add_student, fairy_lights
import re
from unittest.mock import patch
from io import StringIO


def normalize_string(s: str) -> str:
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

class TestAssessment02(unittest.TestCase):
    def setUp(self):
        self.data = {
            "Alice": [80, 90, 100],
            "Bob": [70],
            "Charlie": [],
        }
    # 1
    def test_calculate_average_typical_list(self):
        self.assertAlmostEqual(calculate_average([80, 90, 100]), 90.0)

    # 1
    def test_calculate_average_single_element(self):
        self.assertAlmostEqual(calculate_average([42]), 42.0)

    # 1
    def test_calculate_average_with_zero_in_numbers(self):
        self.assertAlmostEqual(calculate_average([0, 5, 10]), 5.0)

    # 1
    def test_calculate_average_with_empty_list(self):
        self.assertAlmostEqual(calculate_average([]), 0)

    # 1
    def test_get_student_average_student_found_multiple_scores(self):
        self.assertAlmostEqual(get_student_average("Alice", self.data), 90.0)

    # 1
    def test_get_student_average_student_found_single_score(self):
        self.assertAlmostEqual(get_student_average("Bob", self.data), 70.0)

    # 1
    def test_get_student_average_student_found_empty_scores(self):
        self.assertEqual(get_student_average("Charlie", self.data), 0)

    # 1
    def test_get_student_average_student_not_found(self):
        self.assertEqual(get_student_average("Diana", self.data), -1)

    # 2
    def test_get_top_student_normal_case(self):
        data = {
            "Alice": [80, 90, 100],   # avg = 90
            "Bob": [70, 75, 80],      # avg = 75
            "Charlie": [85, 95, 90],  # avg = 90
        }
        self.assertIn(get_top_student(data), ["Alice", "Charlie"])  # both avg = 90

    # 2
    def test_get_top_student_clear_winner(self):
        data = {
            "Alice": [60, 65, 70],
            "Bob": [95, 100, 90],
            "Charlie": [80, 85, 80],
        }
        self.assertEqual(get_top_student(data), "Bob")

    # 2
    def test_get_top_student_with_empty_scores(self):
        data = {
            "Alice": [],
            "Bob": [80],
            "Charlie": [90, 100],
        }
        self.assertEqual(get_top_student(data), "Charlie")

    # 1
    def test_add_student_new(self):
        data = {"Alice": [90, 95]}
        result = add_student(data, "Bob", [80, 85])
        self.assertIn("Bob", result)
        self.assertEqual(result["Bob"], [80, 85])

    # 1
    def test_add_student_existing(self):
        data = {"Alice": [90, 95]}
        result = add_student(data, "Alice", [100, 100])
        self.assertEqual(result["Alice"], [90, 95])

    # 1
    def test_add_student_empty_scores(self):
        data = {}
        result = add_student(data, "Charlie", [])
        self.assertIn("Charlie", result)
        self.assertEqual(result["Charlie"], [])

    # 2
    @patch('builtins.input', side_effect=["r", "g", "b", "q"])
    def test_fairylights_valid_inputs_then_quit(self, mock_input):
        result = fairy_lights()
        self.assertEqual(result, ["r", "g", "b"])

    # 2
    @patch('builtins.input', side_effect=["r", "y", "g", "l", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_fairylights_invalid_inputs_then_valid_then_quit1(self, mock_stdout, mock_input):
        result = fairy_lights()
        self.assertEqual(result, ["r", "g"])
        output = normalize_string(mock_stdout.getvalue())
        self.assertEqual(output.count(normalize_string("invalid input")), 2)

    # 2
    @patch('builtins.input', side_effect=["x", "y", "g", "q"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_fairylights_invalid_inputs_then_valid_then_quit2(self, mock_stdout, mock_input):
        result = fairy_lights()
        self.assertEqual(result, ["g"])
        output = normalize_string(mock_stdout.getvalue())
        self.assertEqual(output.count(normalize_string("invalid input")), 2)

    # 2
    @patch('builtins.input', side_effect=["q"])
    def test_fairylights_immediate_quit(self, mock_input):
        result = fairy_lights()
        self.assertEqual(result, [])
