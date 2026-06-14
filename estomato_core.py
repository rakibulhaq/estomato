import re


_TIME_PATTERN = re.compile(
	r"""
	(?<!\w)
	(?P<prefix>[+-]\s*|\*\s*\d+(?:\.\d+)?\s*)?
	(?P<value>\d+(?:\.\d+)?)
	\s*
	(?P<unit>[dh])
	\b
	""",
	re.IGNORECASE | re.VERBOSE,
)

_CURRENCY_PATTERN = re.compile(
	r"""
	(?<!\w)
	(?P<prefix>[+-]\s*|\*\s*\d+(?:\.\d+)?\s*)?
	(?P<currency>
		USD|BDT|RM|YEN|WON|EUR|GBP|INR|JPY|CNY|AUD|CAD|SGD|HKD|MYR|KRW|THB|PHP|AED|SAR|
		\$|€|£|¥|৳|₹|₩
	)
	\s*
	(?P<value>\d+(?:\.\d+)?)
	""",
	re.IGNORECASE | re.VERBOSE,
)


def _apply_prefix(prefix, value):
	if not prefix:
		return value

	prefix = prefix.strip()
	if prefix.startswith('-'):
		return -value
	if prefix.startswith('*'):
		factor = prefix[1:].strip()
		return value * float(factor or 1)
	return value


def summarize_selection(text, mandaytohour):
	days = 0.0
	hours = 0.0
	currencies = {}

	for match in _TIME_PATTERN.finditer(text):
		amount = _apply_prefix(match.group('prefix'), float(match.group('value')))
		if match.group('unit').lower() == 'd':
			days += amount
		else:
			hours += amount

	for match in _CURRENCY_PATTERN.finditer(text):
		label = match.group('currency')
		if label.isalpha():
			label = label.upper()
		amount = _apply_prefix(match.group('prefix'), float(match.group('value')))
		currencies[label] = currencies.get(label, 0.0) + amount

	total_days = days + (hours / mandaytohour)
	total_hours = (days * mandaytohour) + hours

	return {
		'total_days': total_days,
		'total_hours': total_hours,
		'currencies': currencies,
	}


def build_summary_lines(text, mandaytohour):
	summary = summarize_selection(text, mandaytohour)
	lines = [
		text,
		"------------------------------------------------",
		"Mandays required: {days:.2f} Days".format(days=summary['total_days']),
		"Manhour required: {hour:.2f} Hour".format(hour=summary['total_hours']),
	]

	for currency, amount in summary['currencies'].items():
		lines.append("Amount required [{currency}]: {amount:.2f}".format(
			currency=currency,
			amount=amount,
		))

	lines.append("------------------------------------------------")
	return lines
