# Copyright 2021 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from pathlib import Path
from shutil import rmtree

from towhee.hub.repo_manager import RepoManager

public_path = Path(__file__).parent.parent.resolve()


class TestRepoManager(unittest.TestCase):
    """
    Unit test for RepoManager.
    """
    def test_base(self):
        rm = RepoManager('towhee', 'test-repo')
        self.assertEqual(rm.author, 'towhee')
        self.assertEqual(rm.repo, 'test-repo')
        self.assertEqual(rm.root, 'https://hub.towhee.io')

    def test_exists(self):
        rm_1 = RepoManager('towhee', 'test-repo')
        self.assertFalse(rm_1.exists())

        rm_2 = RepoManager('towhee', 'ci-test')
        self.assertTrue(rm_2.exists())

    def test_clone(self):
        rm = RepoManager('towhee', 'ci-test')
        repo_dir = public_path / 'test_cache' / 'ci_test'
        if repo_dir.is_dir():
            rmtree(repo_dir)
        rm.clone(repo_dir)
        files = [f.name for f in repo_dir.iterdir()]

        self.assertTrue(repo_dir.is_dir())
        self.assertIn('.git', files)
        rmtree(repo_dir)

    def test_download_executor(self):
        rm = RepoManager('towhee', 'ci-test')
        repo_dir = public_path / 'test_cache' / 'ci_test'
        if repo_dir.is_dir():
            rmtree(repo_dir)
        rm.download_executor('main', 'README.md', tuple([]), repo_dir)

        self.assertTrue((repo_dir / 'README.md').is_file())
        rmtree(repo_dir)

    def test_download_files(self):
        rm = RepoManager('towhee', 'ci-test')
        repo_dir = public_path / 'test_cache' / 'ci_test'
        if repo_dir.is_dir():
            rmtree(repo_dir)

        rm.download_files('main', ['README.md'], tuple([]), repo_dir, False)
        self.assertTrue((repo_dir / 'README.md').is_file())
        rmtree(repo_dir)

        # When something goes wrong while download, throe error and delete all the other downloaded files.
        self.assertRaises(Exception, rm.download_files, 'main', ['README.md', 'FileThatNotExists'], tuple([]), repo_dir, False)
        self.assertFalse((repo_dir / 'README.md').is_file())

    def test_download(self):
        rm = RepoManager('towhee', 'ci-test')
        repo_dir = public_path / 'test_cache' / 'ci_test'
        if repo_dir.is_dir():
            rmtree(repo_dir)
        rm.download(repo_dir)
        files = [f.name for f in repo_dir.iterdir()]

        self.assertTrue(repo_dir.is_dir())
        self.assertNotIn('.git', files)
        rmtree(repo_dir)


if __name__ == '__main__':
    unittest.main()