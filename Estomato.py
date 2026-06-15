import sublime
import sublime_plugin

try:
	from .estomato_core import build_summary_lines
except ImportError:
	from estomato_core import build_summary_lines


class EstomatoCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		mandaytohour = round(float(args['mandaytohour']), 1)
		
		if not mandaytohour > 0:
			return

		for region in self.view.sel():
			if not region.empty():
				s = self.view.substr(region)
				lines = build_summary_lines(s, mandaytohour)
				self.view.replace(edit, region, "\n".join(lines))
