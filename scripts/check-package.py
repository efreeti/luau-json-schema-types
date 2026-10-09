"""Verify the exact npm artifact and execute its exported module."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tarfile
root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--luau', default='luau')
parser.add_argument('--analyzer', default='luau-analyze')
args = parser.parse_args()
subprocess.run([sys.executable, str(root / 'scripts/build-package.py')], cwd=root, check=True)
manifest = json.loads((root / 'package.json').read_text())
output = root / manifest['luau']['build']['output']
modules = {p.name for p in (root / 'src').glob('*.luau')}
expected = modules | {'package.json', 'README.md', 'LICENSE'}
if (root / 'NOTICE').exists():
    expected.add('NOTICE')
actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
assert actual == expected, actual ^ expected
published = json.loads((output / 'package.json').read_text())
assert published['version'] == manifest['version'] and published['main'] == 'init.luau'
assert not {'scripts', 'devDependencies', 'luau'} & published.keys()
assert all(not value.startswith('file:') for value in published.get('dependencies', {}).values())
for name in modules:
    assert (output / name).read_bytes() == (root / 'src' / name).read_bytes()
result = subprocess.run(['npm', 'pack', '--json', '--pack-destination', str(root / 'build')],
                        cwd=output, check=True, capture_output=True, text=True)
archive = root / 'build' / json.loads(result.stdout)[0]['filename']
with tarfile.open(archive, 'r:gz') as package:
    assert {m.name.removeprefix('package/') for m in package.getmembers() if m.isfile()} == expected
    for name in expected:
        assert package.extractfile('package/' + name).read() == (output / name).read_bytes()
smoke = root / 'build/package-smoke.luau'
code = '--!strict\nlocal Library = require("./package")\n'
if 'validate.luau' in modules:
    code += 'local schema: Library.JSONSchema = {type="object", required={"name"}, properties={name={type="string"}}}\nassert(Library.validate(schema, {name="Ada"}).valid)\nassert(not Library.validate(schema, {}).valid)\nassert(not Library.validate(schema, {name=42}).valid)\n'
else:
    code += 'local schema: Library.TextJSONSchema = {type="string", format="email"}\nassert(type(schema) == "table")\nassert(next(Library :: {[string]: unknown}) == nil)\n'
smoke.write_text(code)
for tool in (args.analyzer, args.luau):
    executable = str(Path(tool).resolve()) if Path(tool).is_file() else tool
    subprocess.run([executable, str(smoke)], cwd=root, check=True)
print('PASS npm archive, publication metadata, and typed runtime import')
