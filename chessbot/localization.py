"""Module with changing app language functions."""
import os
import locale
import gettext


def set_lang(lang='en'):
    """Set app lang from pre-created gettext files."""
    base_dir = os.path.dirname(__file__)
    transl = gettext.translation('chessbot', base_dir, languages=[lang])
    transl.install()

def set_system_lang():
    """Set lang according to system, english by default."""
    loc, _ = locale.getdefaultlocale()

    if loc is None:
        set_lang()
        return

    if loc.lower().startswith('ru_'):
        set_lang('ru')
        return

    set_lang()
