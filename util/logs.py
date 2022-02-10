import logging
import coloredlogs

fieldstyle = {'asctime': {'color': 'green'},
              'levelname': {'bold': True, 'color': 'white'},
              'filename': {'color': 'cyan'},
              'funcName': {'color': 'blue'},
              'lineno': {'color': 'white'}}

levelstyles = {'critical': {'bold': True, 'color': 'red'},
               'debug': {'color': 'green'},
               'error': {'color': 'red'},
               'info': {'color': 'magenta'},
               'warning': {'color': 'yellow'}}

mylogs = logging.getLogger(__name__)
mylogs.setLevel(logging.DEBUG)
coloredlogs.install(level=logging.DEBUG,
                    logger=mylogs,
                    fmt='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%H:%M:%S',
                    field_styles=fieldstyle,
                    level_styles=levelstyles)
