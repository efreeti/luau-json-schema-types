"""Verify release versions and the Git history they produce without publishing."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

repo = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('release_version', repo / 'scripts/version.py')
version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version)

class ReleaseVersionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.previous_root = version.root
        self.addCleanup(setattr, version, 'root', self.previous_root)
        version.root = Path(self.temporary.name) / 'checkout'
        version.root.mkdir()
        (version.root / 'package.json').write_text('{"name":"example", "version":"1.0.0"}\n')
        (version.root / 'README.md').write_text('Use "@efreeti/luau-json-schema-types@1.0.0"\n')

    def test_valid_development_versions(self):
        for next_version in ('1.0.1', '1.0.1-dev.0', '1.0.1-SNAPSHOT'):
            version.validate('1.0.0', next_version)

    def test_invalid_release_inputs(self):
        for release, next_version in (
            ('1.0.0-dev.0', '1.0.1'), ('1.0.0', '1.0.0'),
            ('1.0.0', '0.9.0'), ('01.0.0', '1.0.1'),
            ('1.0.0', '1.0.1-dev.01'), ('1.0.0\n', '1.0.1'),
            ('1.0.0', '1.0.1; echo unexpected'),
        ):
            with self.subTest(release=release, next_version=next_version):
                with self.assertRaises(ValueError):
                    version.validate(release, next_version)

    def test_invalid_current_version_is_rejected(self):
        (version.root / 'package.json').write_text('{"version":"invalid"}')
        with self.assertRaises(ValueError):
            version.set_version('1.1.0')

    def test_lockfile_version_is_updated(self):
        (version.root / 'package-lock.json').write_text('{"version":"1.0.0", "packages":{"":{"version":"1.0.0"}}}')
        version.set_version('1.1.0')
        lock = json.loads((version.root / 'package-lock.json').read_text())
        self.assertEqual(lock['version'], '1.1.0')
        self.assertEqual(lock['packages']['']['version'], '1.1.0')

    def test_release_and_development_updates(self):
        version.set_version('1.1.0', update_readme=True)
        version.set_version('1.1.1-dev.0')
        self.assertEqual(json.loads((version.root / 'package.json').read_text())['version'], '1.1.1-dev.0')
        self.assertIn('@1.1.0"', (version.root / 'README.md').read_text())

    def test_release_tag_and_next_commit_in_remote(self):
        remote = Path(self.temporary.name) / 'origin.git'
        subprocess.run(['git', 'init', '--bare', str(remote)], check=True, capture_output=True)
        def git(*args):
            return subprocess.run(['git', *args], cwd=version.root, check=True,
                                  capture_output=True, text=True).stdout.strip()
        git('init', '-b', 'main')
        git('config', 'user.name', 'Release test')
        git('config', 'user.email', 'release-test@example.test')
        git('remote', 'add', 'origin', str(remote))
        git('add', '.')
        git('commit', '-m', 'Initial')
        git('push', 'origin', 'main')
        version.set_version('1.1.0', update_readme=True)
        git('add', 'package.json', 'README.md')
        git('commit', '-m', 'Release 1.1.0')
        git('tag', '-a', 'v1.1.0', '-m', 'Release 1.1.0')
        git('push', '--atomic', 'origin', 'HEAD:refs/heads/main', 'refs/tags/v1.1.0')
        version.set_version('1.1.1-dev.0')
        git('add', 'package.json')
        git('commit', '-m', 'Prepare development version 1.1.1-dev.0')
        git('push', 'origin', 'HEAD:refs/heads/main')
        def remote_file(ref, name):
            return subprocess.run(['git', '--git-dir', str(remote), 'show', ref + ':' + name],
                                  check=True, capture_output=True, text=True).stdout
        self.assertEqual(json.loads(remote_file('v1.1.0', 'package.json'))['version'], '1.1.0')
        self.assertEqual(json.loads(remote_file('main', 'package.json'))['version'], '1.1.1-dev.0')
        self.assertIn('@1.1.0"', remote_file('main', 'README.md'))

if __name__ == '__main__':
    unittest.main()
