import unittest

from estomato_core import build_summary_lines, summarize_selection


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
