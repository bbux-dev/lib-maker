import os
import libmaker


def test_makeit(tmpdir):

    libmaker.makeit(outdir=str(tmpdir),
                    name="fluffybunny",
                    author="tester",
                    description="test project creation",
                    email="test@test.com",
                    license="test licence",
                    project="test project name",
                    package="test_package",
                    package_data=None,
                    requirements=["datacraft", "datacraft-xeger", "datacraft-geo"],
                    script="testit",
                    url="https://testit.test.testing/fluffybunny",
                    version="1.2.3")

    assert os.path.exists(tmpdir / 'fluffybunny')
    root_files = os.listdir(tmpdir / 'fluffybunny')
    expected = ['.gitignore', 'pyproject.toml', 'README.md', 'setup.cfg', 'setup.py', 'tests', 'test_package']

    assert len(root_files) == len(expected), f'Expected {len(expected)} files in root but was {len(root_files)}'
    for file in root_files:
        assert file in expected, f'File: {file} not expected to be in root directory!'
