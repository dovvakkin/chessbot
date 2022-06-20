#!/usr/bin/env python3
'''
Default: create wheel
'''
import glob
from doit.tools import create_folder

DOIT_CONFIG = {'default_tasks': ['all']}


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
            'actions': ['git clean -xdf'],
           }


def task_html():
    """Make HTML documentation."""
    return {
            'actions': ['sphinx-build -M html docs build'],
           }


def task_test():
    """Preform tests."""
    yield {'actions': ['pytest'], 'name': "test"}




def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o chessbot.pot chessbot'],
            'file_dep': glob.glob('chessbot/*.py'),
            'targets': ['chessbot.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D chessbot -d po -i chessbot.pot'],
            'file_dep': ['chessbot.pot'],
            'targets': ['po/ru/LC_MESSAGES/chessbot.po'],
           }


def task_mo():
    """Compile translations."""
    langs = ['en', 'ru']
    return {
            'actions': [
                (create_folder, [f'chessbot/{lang}/LC_MESSAGES']) for lang in langs
                       ] +
                       [
    f'pybabel compile -D chessbot -l {lang} -i po/{lang}/LC_MESSAGES/chessbot.po -d chessbot' for lang in langs
                       ],
            'file_dep': [
                f'po/{lang}/LC_MESSAGES/chessbot.po' for lang in langs
                        ],
            'targets': [
                f'chessbot/{lang}/LC_MESSAGES/chessbot.mo' for lang in langs
                       ],
           }


def task_get_stockfish():
    """Download stockfish binary."""
    return {
            'actions': ['python chessbot/stockfish_downloader.py']
           }


def task_sdist():
    """Create source distribution."""
    return {
            'actions': ['python -m build -s'],
            'task_dep': ['gitclean', 'mo'],
           }


def task_wheel():
    """Create binary wheel distribution."""
    return {
            'actions': ['python -m build -w'],
            'task_dep': ['mo', 'get_stockfish'],
           }


def task_app():
    """Run application."""
    return {
            'actions': ['python -m chessbot'],
            'task_dep': ['mo'],
           }
