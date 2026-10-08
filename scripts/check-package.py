"""Verify distributable archive contents and matching Wally/npm versions."""
from pathlib import Path
import json, subprocess, sys, tomllib, zipfile
root = Path(__file__).resolve().parents[1]
wally = sys.argv[1] if len(sys.argv) > 1 else 'wally'
manifest = tomllib.loads((root / 'wally.toml').read_text())
assert manifest['package']['version'] == json.loads((root / 'package.json').read_text())['version']
(root / 'build').mkdir(exist_ok=True)
archive = root / 'build/package.zip'
archive.unlink(missing_ok=True)
subprocess.run([wally, 'package', '--output', str(archive)], cwd=root, check=True)
with zipfile.ZipFile(archive) as package:
    files = {name.removeprefix('./') for name in package.namelist() if not name.endswith('/')}
    expected = {'wally.toml', 'default.project.json', 'src/init.luau', 'src/types.luau', 'README.md', 'LICENSE', 'NOTICE'}
    assert files == expected, f'Unexpected package contents: {files ^ expected}'
print('PASS Wally package contents and version consistency')
