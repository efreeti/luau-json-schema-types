"""Check schema construction types and native Luau representations."""
import argparse, pathlib, subprocess, sys
root = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--luau', default='luau')
parser.add_argument('--analyzer', default='luau-analyze')
args = parser.parse_args()
subprocess.run([sys.executable, str(root / "scripts/generate-fixtures.py")], cwd=root, check=True)
subprocess.run([args.analyzer, 'src/init.luau', 'src/types.luau', 'tests/FixtureData.luau', 'tests/run.luau', 'tests/types-positive.luau'], cwd=root, check=True)
negative = subprocess.run([args.analyzer, 'tests/types-negative.luau'], cwd=root, text=True, capture_output=True)
assert negative.returncode != 0 and negative.stderr.count('TypeError') >= 6, 'Negative type tests were not rejected: ' + negative.stderr
subprocess.run([args.luau, 'tests/run.luau'], cwd=root, check=True)
print('PASS positive schema construction and 6 negative type checks')
