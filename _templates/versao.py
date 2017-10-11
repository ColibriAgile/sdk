from datetime import date
try:
    from __buildnumber__ import BUILD_NUMBER, DEVELOP
except (ImportError, ValueError) as e:
    BUILD_NUMBER = 0
    DEVELOP = True
from __version__ import MAJOR, MINOR, RELEASE


VERSION = (MAJOR, MINOR, RELEASE, BUILD_NUMBER)


def version_info():
    return dict(
        company='NCR Food Service',
        name='NCR Colibri Master',
        fileversion='.'.join(str(x) for x in VERSION),
        version='.'.join(str(x) for x in VERSION[:3]),
        build_number=BUILD_NUMBER,
        year=date.today().year,
        develop=DEVELOP
    )
