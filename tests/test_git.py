import pytest
import pytest_git
# pytest_plugins = ['pytest_git']
from pytest_git import GitRepo

def test_always_passes(git_repo: GitRepo):
    print(git_repo)
    path = git_repo.workspace
    file = path / 'hello.txt'
    f = file.write_text('test')
    assert True

def test_always_fails():
    assert False