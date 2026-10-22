import sublime
import sublime_plugin

try:
	from .estomato_core import build_summary_lines, resolve_mandaytohour
except ImportError:
	from estomato_core import build_summary_lines, resolve_mandaytohour


SETTINGS_FILE = 'Estomato.sublime-settings'


class EstomatoCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		settings = sublime.load_settings(SETTINGS_FILE)
		mandaytohour = resolve_mandaytohour(
			args.get('mandaytohour'),
			settings.get('mandaytohour'),
		)

		if mandaytohour is None:
			sublime.status_message("Estomato: mandaytohour must be a positive number")
			return

		for region in self.view.sel():
			if not region.empty():
				s = self.view.substr(region)
				lines = build_summary_lines(s, mandaytohour)
				self.view.replace(edit, region, "\n".join(lines))
