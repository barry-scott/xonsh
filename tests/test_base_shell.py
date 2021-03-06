# -*- coding: utf-8 -*-
"""(A down payment on) Testing for ``xonsh.base_shell.BaseShell`` and associated classes"""
import os
import builtins

import pytest

from xonsh import dirstack
from xonsh.environ import Env
from xonsh.built_ins import load_builtins
from xonsh.base_shell import BaseShell


def test_pwd_tracks_cwd(xonsh_builtins, xonsh_execer, tmpdir_factory, monkeypatch ):
    asubdir = str(tmpdir_factory.mktemp("asubdir"))
    cur_wd = os.getcwd()
    xonsh_builtins.__xonsh_env__ = Env(PWD=cur_wd, XONSH_CACHE_SCRIPTS=False, XONSH_CACHE_EVERYTHING=False)

    monkeypatch.setattr(xonsh_execer, "cacheall", False, raising=False)
    bc = BaseShell(xonsh_execer, None)

    assert os.getcwd() == cur_wd

    bc.default('os.chdir(r"' + asubdir + '")')

    assert os.path.abspath(os.getcwd()) == os.path.abspath(asubdir)
    assert os.path.abspath(os.getcwd()) == os.path.abspath(xonsh_builtins.__xonsh_env__['PWD'])

