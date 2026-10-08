"""Validate release inputs and update the package manifests together."""
import argparse
import json
from pathlib import Path
import re
import tomllib

root = Path(__file__).resolve().parents[1]
# Wally and npm both use SemVer; a Maven-style development version can be
# expressed as a prerelease, e.g. 1.0.1-dev.0 or 1.0.1-SNAPSHOT.
number = r'(?:0|[1-9][0-9]*)'
identifier = r'(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)'
version_pattern = re.compile(
    rf'({number})\.({number})\.({number})(?:-({identifier}(?:\.{identifier})*))?'
)

def parse_version(value):
    match = version_pattern.fullmatch(value)
    if not match:
        raise ValueError(f'Invalid version {value!r}; use MAJOR.MINOR.PATCH with an optional prerelease')
    return tuple(int(match[i]) for i in (1, 2, 3)), match[4]

def manifests():
    wally_path = root / 'wally.toml'
    npm_path = root / 'package.json'
    wally = wally_path.read_text()
    npm = json.loads(npm_path.read_text())
    current = tomllib.loads(wally)['package']['version']
    if npm['version'] != current:
        raise ValueError('wally.toml and package.json must have the same version')
    return wally_path, npm_path, wally, npm

def validate(release, next_version):
    release_core, prerelease = parse_version(release)
    next_core, _ = parse_version(next_version)
    if prerelease:
        raise ValueError('The published release must be a stable MAJOR.MINOR.PATCH version')
    if next_core <= release_core:
        raise ValueError('The next development version must have a higher MAJOR.MINOR.PATCH than the release')
    manifests()

def set_version(value, update_readme=False):
    parse_version(value)
    wally_path, npm_path, wally, npm = manifests()
    # Edit only the package section; dependency versions remain untouched.
    start = re.search(r'^\[package\]\s*$', wally, re.MULTILINE)
    if start is None:
        raise ValueError('Missing Wally package section')
    rest = wally[start.end():]
    following = re.search(r'^\[', rest, re.MULTILINE)
    end = start.end() + following.start() if following else len(wally)
    section, count = re.subn(r'^(version\s*=\s*)"[^"]+"', lambda m: m[1] + json.dumps(value),
                            wally[start.end():end], flags=re.MULTILINE)
    if count != 1:
        raise ValueError('Expected one version in the Wally package section')
    updated = wally[:start.end()] + section + wally[end:]
    assert tomllib.loads(updated)['package']['version'] == value
    npm['version'] = value
    wally_path.write_text(updated)
    npm_path.write_text(json.dumps(npm, indent=2) + '\n')
    if update_readme:
        path = root / 'README.md'
        text = re.sub(r'efreeti/json-schema-types@[^"\s]+',
                      lambda _: 'efreeti/json-schema-types@' + value, path.read_text())
        path.write_text(text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('validate')
    check.add_argument('release_version')
    check.add_argument('next_version')
    setter = commands.add_parser('set')
    setter.add_argument('version')
    setter.add_argument('--update-readme', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'validate':
            validate(args.release_version, args.next_version)
        else:
            set_version(args.version, args.update_readme)
    except ValueError as error:
        parser.error(str(error))
