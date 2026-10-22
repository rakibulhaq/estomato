import json
import os
import re
import unittest

from estomato_core import (
	DEFAULT_MANDAYTOHOUR,
	build_summary_lines,
	resolve_mandaytohour,
	summarize_selection,
)


HERE = os.path.dirname(os.path.abspath(__file__))


def _load_sublime_json(name):
	# Sublime resource files allow // comments and trailing commas.
	with open(os.path.join(HERE, name)) as f:
		text = f.read()
	text = re.sub(r'^\s*//.*$', '', text, flags=re.MULTILINE)
	text = re.sub(r',(\s*[\]}])', r'\1', text)
	return json.loads(text)


class ResolveMandaytohourTests(unittest.TestCase):
	def test_defaults_to_six_and_a_half_hours(self):
		self.assertEqual(DEFAULT_MANDAYTOHOUR, 6.5)
		self.assertEqual(resolve_mandaytohour(), 6.5)

	def test_uses_setting_when_no_arg_is_given(self):
		self.assertEqual(resolve_mandaytohour(None, 8), 8.0)

	def test_arg_overrides_setting(self):
		self.assertEqual(resolve_mandaytohour("7.5", 8), 7.5)

	def test_accepts_numeric_strings_and_rounds_to_one_decimal(self):
		self.assertEqual(resolve_mandaytohour(None, "7"), 7.0)
		self.assertEqual(resolve_mandaytohour(None, 7.04), 7.0)

	def test_rejects_invalid_values(self):
		for value in (0, -1, "abc", "", [], True, False):
			self.assertIsNone(resolve_mandaytohour(None, value), value)
			self.assertIsNone(resolve_mandaytohour(value, 8), value)

	def test_setting_value_drives_summary(self):
		mandaytohour = resolve_mandaytohour(None, 8)
		lines = build_summary_lines("api 4h\ndocs 1d", mandaytohour)

		self.assertIn("Mandays required: 1.50 Days", lines)
		self.assertIn("Manhour required: 12.00 Hour", lines)


class PackageResourceTests(unittest.TestCase):
	def test_settings_file_ships_default(self):
		settings = _load_sublime_json('Estomato.sublime-settings')

		self.assertEqual(settings['mandaytohour'], DEFAULT_MANDAYTOHOUR)

	def test_run_command_does_not_hardcode_mandaytohour(self):
		commands = _load_sublime_json('Default.sublime-commands')
		run = next(c for c in commands if c['command'] == 'estomato')

		self.assertNotIn('mandaytohour', run.get('args', {}))


class SummarizeSelectionTests(unittest.TestCase):
	def test_preserves_existing_day_and_hour_summary(self):
		summary = summarize_selection("init 2h\napi 3h\ndocs 1d", 6.5)

		self.assertAlmostEqual(summary['total_days'], 1 + (5 / 6.5))
		self.assertAlmostEqual(summary['total_hours'], 11.5)
		self.assertEqual(summary['currencies'], {})

	def test_supports_currency_detection_and_prefixed_operators(self):
		text = "\n".join([
			"base $10",
			"discount -$2",
			"bonus +$5",
			"bulk *3 $4",
			"budget USD 20",
			"refund - USD 5",
			"team * 2 USD 3",
			"estimate 2h",
			"adjust -1h",
			"rollout *2 0.5d",
		])

		summary = summarize_selection(text, 8)
		lines = build_summary_lines(text, 8)

		self.assertAlmostEqual(summary['currencies']['$'], 25.0)
		self.assertAlmostEqual(summary['currencies']['USD'], 21.0)
		self.assertAlmostEqual(summary['total_hours'], 9.0)
		self.assertAlmostEqual(summary['total_days'], 1.125)
		self.assertIn("Amount required [$]: 25.00", lines)
		self.assertIn("Amount required [USD]: 21.00", lines)


if __name__ == '__main__':
	unittest.main()
