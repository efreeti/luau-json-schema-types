"""Validate release inputs and update npm package and lockfile versions."""
import argparse
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
# npm uses SemVer; a Maven-style development version can be
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
    path = root / 'package.json'
    npm = json.loads(path.read_text())
    parse_version(npm['version'])
    return path, npm

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
    path, npm = manifests()
    npm['version'] = value
    path.write_text(json.dumps(npm, indent=2) + '\n')
    lock_path = root / 'package-lock.json'
    if lock_path.exists():
        lock = json.loads(lock_path.read_text())
        lock['version'] = value
        lock['packages']['']['version'] = value
        lock_path.write_text(json.dumps(lock, indent=2) + '\n')
    if update_readme:
        path = root / 'README.md'
        text = re.sub(r'@efreeti/luau-json-schema-types@[^"\s]+',
                      lambda _: '@efreeti/luau-json-schema-types@' + value, path.read_text())
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
