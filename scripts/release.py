"""Version and update-message helper for the Makefile.

Package Control picks up releases from semver git tags (vX.Y.Z) and shows
messages/<version>.txt to users who upgrade, as listed in messages.json.
"""

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESSAGES_JSON = os.path.join(ROOT, 'messages.json')
MESSAGES_DIR = os.path.join(ROOT, 'messages')
PLACEHOLDER = '<describe the changes in this release>'
SEMVER = re.compile(r'^v?(\d+)\.(\d+)\.(\d+)$')


def fail(msg):
	sys.stderr.write('error: %s\n' % msg)
	sys.exit(1)


def git(*args):
	return subprocess.check_output(('git',) + args, cwd=ROOT, text=True).strip()


def parse(version):
	match = SEMVER.match(version)
	if not match:
		fail('not a semver version: %s' % version)
	return tuple(int(part) for part in match.groups())


def fmt(parts):
	return '%d.%d.%d' % parts


def current_version():
	tags = [tag for tag in git('tag', '--list', 'v*').split() if SEMVER.match(tag)]
	if not tags:
		return '0.0.0'
	return fmt(max(parse(tag) for tag in tags))


def next_version(part):
	major, minor, patch = parse(current_version())
	if part == 'major':
		return fmt((major + 1, 0, 0))
	if part == 'minor':
		return fmt((major, minor + 1, 0))
	if part == 'patch':
		return fmt((major, minor, patch + 1))
	fail('unknown part: %s (expected major, minor or patch)' % part)


def load_messages():
	if not os.path.exists(MESSAGES_JSON):
		return {}
	with open(MESSAGES_JSON) as f:
		return json.load(f)


def save_messages(messages):
	# Package Control lists "install" first, then versions in order.
	ordered = {}
	if 'install' in messages:
		ordered['install'] = messages['install']
	for key in sorted((k for k in messages if k != 'install'), key=parse):
		ordered[key] = messages[key]
	with open(MESSAGES_JSON, 'w') as f:
		json.dump(ordered, f, indent='\t')
		f.write('\n')


def pending_version():
	"""Highest version registered in messages.json that is not tagged yet."""
	current = parse(current_version())
	versions = [parse(k) for k in load_messages() if k != 'install']
	pending = [v for v in versions if v > current]
	if not pending:
		fail('no untagged version in messages.json; run make bump-patch/minor/major first')
	return fmt(max(pending))


def message(version):
	version = fmt(parse(version))
	rel_path = 'messages/%s.txt' % version
	path = os.path.join(ROOT, rel_path)
	if not os.path.exists(path):
		os.makedirs(MESSAGES_DIR, exist_ok=True)
		title = 'Estomato %s' % version
		with open(path, 'w') as f:
			f.write('%s\n%s\n\n%s\n' % (title, '=' * len(title), PLACEHOLDER))
		print('created %s' % rel_path)
	messages = load_messages()
	if messages.get(version) != rel_path:
		messages[version] = rel_path
		save_messages(messages)
		print('registered %s in messages.json' % version)
	print(rel_path)


def check_release():
	version = pending_version()
	if git('status', '--porcelain'):
		fail('working tree is not clean; commit the version bump first')
	path = os.path.join(ROOT, load_messages()[version])
	if not os.path.exists(path):
		fail('missing %s' % path)
	with open(path) as f:
		if PLACEHOLDER in f.read():
			fail('%s still has the placeholder text' % os.path.relpath(path, ROOT))
	print(version)


def main(argv):
	if len(argv) < 2:
		fail('usage: release.py current|next <part>|message <version>|pending|check')
	command = argv[1]
	if command == 'current':
		print(current_version())
	elif command == 'next' and len(argv) == 3:
		print(next_version(argv[2]))
	elif command == 'message' and len(argv) == 3:
		message(argv[2])
	elif command == 'pending':
		print(pending_version())
	elif command == 'check':
		check_release()
	else:
		fail('unknown command: %s' % ' '.join(argv[1:]))


if __name__ == '__main__':
	main(sys.argv)
