"""Create a flat npm publication directory using package.json's files selection."""
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tarfile
import tempfile

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'package.json').read_text())
settings = manifest['luau']['build']
source = PurePosixPath(settings['source'])
output = (root / settings['output']).resolve()
if source.is_absolute() or '..' in source.parts or source == PurePosixPath('.'):
    raise ValueError('Source must be a relative subdirectory')
if not output.is_relative_to(root / 'build') or output == root / 'build':
    raise ValueError('Output must be a subdirectory of build/')
with tempfile.TemporaryDirectory(prefix='luau-package-') as temporary:
    result = subprocess.run(['npm', 'pack', '--json', '--pack-destination', temporary], cwd=root,
                            check=True, capture_output=True, text=True)
    archive = Path(temporary) / json.loads(result.stdout)[0]['filename']
    stage = Path(temporary) / 'output'
    stage.mkdir()
    destinations = set()
    with tarfile.open(archive, 'r:gz') as package:
        for member in package.getmembers():
            if member.isdir():
                continue
            if not member.isfile():
                raise ValueError(f'Unsupported archive entry: {member.name}')
            name = PurePosixPath(member.name).relative_to('package')
            if '..' in name.parts or name.is_absolute():
                raise ValueError(f'Invalid archive path: {name}')
            target = name.relative_to(source) if name.is_relative_to(source) else name
            if target in destinations:
                raise ValueError(f'Flattening would overwrite {target}')
            destinations.add(target)
            destination = stage / target
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(package.extractfile(member).read())
    published = {key: value for key, value in manifest.items()
                 if key not in ('scripts', 'devDependencies', 'luau')}
    published['main'] = 'init.luau'
    published['files'] = sorted(str(name) for name in destinations if str(name) != 'package.json')
    # Local development dependencies become registry dependencies in the artifact.
    for name, requirement in list(published.get('dependencies', {}).items()):
        if requirement.startswith('file:'):
            dependency = json.loads((root / requirement[5:] / 'package.json').read_text())
            if dependency['name'] != name:
                raise ValueError(f'Dependency name mismatch: {name}')
            published['dependencies'][name] = dependency['version']
    (stage / 'package.json').write_text(json.dumps(published, indent=2) + '\n')
    if not (stage / 'init.luau').is_file():
        raise ValueError('Selected source must include init.luau')
    if output.exists():
        shutil.rmtree(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(stage, output)
print(f'Built {output.relative_to(root)}')
