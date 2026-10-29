"""Isolated intake regressions; no observer, network, or production records."""
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Engine'))
import IntakeGear as intake


class IntakeValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'nodes'
        self.outside = self.base / 'outside'
        self.outside.mkdir()
        self.sentinel = self.outside / 'sentinel.json'
        self.sentinel.write_text('unchanged')

    def answers(self, acronym='acme', company='000123', partner='98765432109876543210', scores=('75',)):
        return ['Synthetic agency', acronym, company, partner, 'High', *scores, 'Low', '']

    def run_intake(self, answers):
        with patch.dict(os.environ, {'NFE_NODES_ROOT': str(self.root)}), patch('builtins.input', side_effect=answers), contextlib.redirect_stdout(io.StringIO()):
            intake.run_intake()

    def tree(self):
        return sorted((str(p.relative_to(self.base)), p.read_bytes() if p.is_file() else None)
                      for p in self.base.rglob('*'))

    def test_valid_ids_preserve_strings_and_legacy_filename(self):
        self.run_intake(self.answers())  # Real ScoringGear, no observer.
        path = self.root / 'ACME-000123.98765432109876543210.json'
        data = json.loads(path.read_text())
        self.assertEqual(data['hubspot'], {'company_id': '000123', 'partner_id': '98765432109876543210', 'acronym': 'ACME'})
        self.assertEqual(data['system_id'], path.stem)
        self.assertEqual(data['execution_fit']['match_score'], 75)
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_safe_compatibility_tokens_and_whitespace(self):
        self.assertEqual(intake.build_system_id(' ab-c_2 ', ' A12-03 ', ' p_004 '),
                         ('AB-C_2-A12-03.p_004', 'AB-C_2', 'A12-03', 'p_004'))

    def test_malicious_identifiers_rejected_without_any_filesystem_change(self):
        bad = ['', ' ', '..', '../outside/sentinel', '/tmp/escape', r'..\outside',
               'a/b', 'a\\b', 'a.b', 'a%2fb', 'a:b', 'a b', 'a\nB', 'a\x00b',
               'é', 'ß', 'Ａ', '-abc', '_abc', 'x' * 256]
        before = self.tree()
        for value in bad:
            for index in range(3):
                args = ['ACME', '123', '456']
                args[index] = value
                with self.subTest(value=repr(value), field=index), self.assertRaises(ValueError):
                    self.run_intake(self.answers(*args))
                self.assertEqual(self.tree(), before)
                self.assertFalse(self.root.exists())

    def test_non_text_identifiers(self):
        for value in (None, 123, True, [], {}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                intake.build_system_id(value, '123', '456')

    def test_filename_limit_and_direct_system_id_validation(self):
        valid = 'A-' + '1' * 246 + '.2'
        self.assertEqual(len(intake.node_filename(valid)), 255)
        for value in (valid + '2', '../escape', '/escape', 'A-1.2/escape', 'A-1.2.json', None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                intake.save_node(str(self.root), {'system_id': value})
        self.assertFalse(self.root.exists())

    def test_score_boundaries(self):
        for value, expected in [('0', 0), ('100', 100), (' 50 ', 50), ('000', 0)]:
            with self.subTest(value=value):
                self.assertEqual(intake.match_score(value), expected)
        for value in ('-1', '101', '999', '1.5', 'nan', 'inf', '', '1e2', '+1', '1_0', '１２', '9' * 1000, None, True, 50):
            with self.subTest(value=value), self.assertRaises(ValueError):
                intake.match_score(value)

    def test_persisted_score_endpoints(self):
        for value in ('0', '100'):
            with self.subTest(value=value):
                self.run_intake(self.answers(company=value, scores=(value,)))
                path = self.root / f'ACME-{value}.98765432109876543210.json'
                self.assertEqual(json.loads(path.read_text())['execution_fit']['match_score'], int(value))

    def test_new_file_inserted_after_containment_check_is_preserved(self):
        real_open_root = intake.open_nodes_root
        path = self.root / 'ACME-000123.98765432109876543210.json'
        def insert_file(root):
            fd = real_open_root(root)
            path.write_text('concurrent record')
            return fd
        with patch.object(intake, 'open_nodes_root', side_effect=insert_file), self.assertRaises(FileExistsError):
            self.run_intake(self.answers())
        self.assertEqual(path.read_text(), 'concurrent record')

    def test_invalid_scores_reprompt_before_write(self):
        self.run_intake(self.answers(scores=('-1', '101', 'bad', '100')))
        self.assertEqual(json.loads(next(self.root.glob('*.json')).read_text())['execution_fit']['match_score'], 100)

    def test_interrupted_or_malformed_input_cannot_write(self):
        for answers in [self.answers()[:n] + [EOFError()] for n in range(len(self.answers()))]:
            with self.subTest(length=len(answers)), self.assertRaises(EOFError):
                self.run_intake(answers)
            self.assertFalse(self.root.exists())
        with self.assertRaises(TypeError):
            intake.save_node(str(self.root), {'system_id': 'A-1.2', 'invalid': object()})
        self.assertFalse(self.root.exists())

    def test_existing_record_never_overwritten_and_not_scored(self):
        self.root.mkdir()
        path = self.root / 'ACME-000123.98765432109876543210.json'
        path.write_text('original')
        with patch.object(intake, 'ScoringGear') as scoring, self.assertRaises(FileExistsError):
            self.run_intake(self.answers())
        scoring.assert_not_called()
        self.assertEqual(path.read_text(), 'original')

    def test_existing_symlink_directory_and_hardlink_preserved(self):
        self.root.mkdir()
        path = self.root / 'ACME-000123.98765432109876543210.json'
        for kind in ('symlink', 'dangling', 'directory', 'hardlink'):
            if kind == 'symlink':
                path.symlink_to(self.sentinel)
            elif kind == 'dangling':
                path.symlink_to(self.outside / 'absent')
            elif kind == 'directory':
                path.mkdir()
            else:
                os.link(self.sentinel, path)
            with self.subTest(kind=kind), self.assertRaises((ValueError, FileExistsError)):
                self.run_intake(self.answers())
            self.assertEqual(self.sentinel.read_text(), 'unchanged')
            self.assertFalse((self.outside / 'absent').exists())
            path.rmdir() if kind == 'directory' else path.unlink()

    def test_root_or_ancestor_symlink_cannot_redirect_write(self):
        self.root.symlink_to(self.outside, target_is_directory=True)
        for root in (self.root, self.root / 'nested'):
            with patch.dict(os.environ, {'NFE_NODES_ROOT': str(root)}), patch('builtins.input', side_effect=self.answers()), contextlib.redirect_stdout(io.StringIO()), self.assertRaises(OSError):
                intake.run_intake()
        self.assertEqual(list(self.outside.iterdir()), [self.sentinel])

    def test_destination_symlink_inserted_after_containment_check(self):
        real_open_root = intake.open_nodes_root
        path = self.root / 'ACME-000123.98765432109876543210.json'
        def insert_link(root):
            fd = real_open_root(root)
            path.symlink_to(self.sentinel)
            return fd
        with patch.object(intake, 'open_nodes_root', side_effect=insert_link), self.assertRaises(FileExistsError):
            self.run_intake(self.answers())
        self.assertEqual(self.sentinel.read_text(), 'unchanged')

    def test_root_symlink_swap_after_containment_check(self):
        self.root.mkdir()
        real_open_root = intake.open_nodes_root
        def swap_root(root):
            self.root.rmdir()
            self.root.symlink_to(self.outside, target_is_directory=True)
            return real_open_root(root)
        with patch.object(intake, 'open_nodes_root', side_effect=swap_root), self.assertRaises(OSError):
            self.run_intake(self.answers())
        self.assertEqual(list(self.outside.iterdir()), [self.sentinel])

    def test_relative_configured_root_and_nested_creation(self):
        with patch('os.getcwd', return_value=str(self.base)):
            path = intake.save_node('private/nodes', {'system_id': 'A-1.2'})
        self.assertEqual(Path(path), self.base / 'private/nodes/A-1.2.json')
        self.assertEqual(json.loads(Path(path).read_text()), {'system_id': 'A-1.2'})

    def test_exact_maximum_filename_is_writable(self):
        system_id = 'A-' + '1' * 246 + '.2'
        path = intake.save_node(str(self.root), {'system_id': system_id})
        self.assertEqual(len(Path(path).name), 255)
        self.assertTrue(Path(path).is_file())

    def test_unsupported_platform_fails_before_root_creation(self):
        with patch.object(os, 'supports_dir_fd', set()), self.assertRaises(RuntimeError):
            self.run_intake(self.answers())
        self.assertFalse(self.root.exists())

    def test_missing_config_does_not_write_or_score(self):
        with patch.dict(os.environ, {'NFE_NODES_ROOT': ''}), patch('builtins.input', side_effect=self.answers()), patch.object(intake, 'ScoringGear') as scoring, contextlib.redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError):
            intake.run_intake()
        scoring.assert_not_called()
        self.assertFalse(self.root.exists())


if __name__ == '__main__':
    unittest.main()
