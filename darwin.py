import re
import sys
import traceback
from darwin.cli import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    try:
        main()
    except BaseException as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
