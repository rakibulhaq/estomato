import sublime
import sublime_plugin
import re


class EstomatoCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		mandaytohour = round(float(args['mandaytohour']), 1)
		
		if not mandaytohour > 0:
			return

		regex = r"[\d][\.\d]*(\d+)?[d|h]"
		for region in self.view.sel():
			if not region.empty():
				days = []
				hours = []
				s = self.view.substr(region)
				matches = re.finditer(regex, s, re.MULTILINE | re.IGNORECASE)
				for matchNum, match in enumerate(matches, start=1):
					stamp = match.group().lower()
					length = len(stamp)
					if 'd' in stamp:
						days.append(stamp[:length-1])
					elif 'h' in stamp:
						hours.append(stamp[:length-1])
				subTotalDays = sum(map(float,days))
				subTotalHour = sum(map(float, hours))
				totalDays = subTotalDays + (subTotalHour / mandaytohour)
				totalHour = (subTotalDays*mandaytohour) + subTotalHour
				lines = [
				s, 
				"------------------------------------------------", 
				"Mandays required: {days:.2f} Days".format(days=totalDays), 
				"Manhour required: {hour:.2f} Hour".format(hour=totalHour),
				"------------------------------------------------"
				]
				self.view.replace(edit, region, "\n".join(lines))
