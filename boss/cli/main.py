
import os
import sys
from tempfile import mkdtemp
from cement.core.foundation import CementApp
from cement.core import exc as cement_exc
from cement.utils import fs, misc
from boss.core import exc as boss_exc

CONFIG_DEFAULTS = misc.init_defaults('boss', 'answers')
CONFIG_DEFAULTS['boss']['data_dir'] = '~/.boss/'

class BossApp(CementApp):
    class Meta:
        label = 'boss'
        bootstrap = 'boss.cli.bootstrap'
        config_defaults = CONFIG_DEFAULTS

    def validate_config(self):
        # fix up paths
        self.config.set('boss', 'data_dir',
                        fs.abspath(self.config.get('boss', 'data_dir')))

        # create directories
        if not os.path.exists(self.config.get('boss', 'data_dir')):
            os.makedirs(self.config.get('boss', 'data_dir'))

        # add shortcuts
        pth = os.path.join(self.config.get('boss', 'data_dir'), 'cache')
        if not os.path.exists(fs.abspath(pth)):
            os.makedirs(fs.abspath(pth))
        self.config.set('boss', 'cache_dir', pth)

        pth = os.path.join(self.config.get('boss', 'data_dir'), 'boss.db')
        self.config.set('boss', 'db_path', pth)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    with BossApp(argv=argv) as app:
        try:
            app.run()
        except boss_exc.BossTemplateError as e:
            print("BossTemplateError: %s" % e.msg)
            app.exit_code = 1
        except boss_exc.BossArgumentError as e:
            print("BossArgumentError: %s" % e.msg)
            app.exit_code = 1
        except cement_exc.CaughtSignal as e:        # pragma: nocover
            print(e)                                # pragma: nocover
        except cement_exc.FrameworkError as e:      # pragma: nocover
            print(e)                                # pragma: nocover
            app.exit_code = 1                       # pragma: nocover


if __name__ == '__main__':
    main()  # pragma: nocover
