import os
import locale
import gettext


def set_lang(lang='en'):
    base_dir = os.path.dirname(__file__)
    transl = gettext.translation('chessbot', base_dir, languages=[lang])
    transl.install()

def set_system_lang():
    loc, _ = locale.getdefaultlocale()

    if loc is None:
        set_lang()
        return

    if loc.lower().startswith('ru_'):
        set_lang('ru')
        return

    set_lang()
