import os
import tempfile

import botcontroller


class TestConfigWrite(object):
    @classmethod
    def setup_class(cls):
        cls._controller = botcontroller.BotController()
        cls._config_path = os.path.dirname(os.path.realpath(__file__))
        cls._config_file_valid = os.path.join(cls._config_path, "valid.config")

    def test_writeconfig(self):
        self._controller.load_config(self._config_file_valid)
        outfile = tempfile.TemporaryFile(mode="w")
        self._controller.write_config(outfile)
        outfile.close()
