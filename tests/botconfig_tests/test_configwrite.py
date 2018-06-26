import os
import tempfile

import pytest

import botcontroller


class TestConfigWrite(object):
    @classmethod
    def setup_class(cls):
        cls._controller = botcontroller.BotController()
        cls._config_path = os.path.dirname(os.path.realpath(__file__))
        cls._config_file_valid = os.path.join(cls._config_path, "valid.config")

    def _reload(self):
        with tempfile.TemporaryFile("r+") as outfile:
            self._controller.config.save_config(outfile)
            self._controller.config.load_config(outfile)

    def test_writeconfig(self):
        self._controller.config.load_config(open(self._config_file_valid))
        with tempfile.TemporaryFile("r+") as outfile:
            self._controller.config.save_config(outfile)
            outfile.seek(0)
            self._controller.config.load_config(outfile)

    # Altough you can't change the token by commands, it's a good test if the save works - and every
    # config data which can be loaded should be saved, too (even if immutable)
    def test_changetoken(self):
        test_token = "123:45"
        self._controller.config.load_config(open(self._config_file_valid))
        self._controller.config._telegram_token = test_token
        self._reload()
        assert test_token == self._controller.config._telegram_token

    def test_adduser(self):
        test_id = "4711"
        self._controller.config.load_config(open(self._config_file_valid))
        self._controller.add_access(test_id)
        self._reload()
        assert self._controller.has_access(test_id)

    def test_removeuser(self):
        test_id = "543431"
        self._controller.config.load_config(open(self._config_file_valid))
        self._controller.remove_access(test_id)
        self._reload()
        assert not self._controller.has_access(test_id)
        assert self._controller.has_access("12354")

    # See test_changetoken()
    def test_change_spotify_username(self):
        test_username = "MyNewUsername"
        self._controller.config.load_config(open(self._config_file_valid))
        self._controller.config._spotify_username = test_username
        self._reload()
        assert test_username == self._controller.config._spotify_username

    @pytest.mark.parametrize("bookmark_name, track_id, playlist_id", (
            ("current", "12345abcdef", None),
            ("current", "abcdefg", "hijklmno"),
            ("alpha", "1111111111", None)
    ))
    def test_change_bookmark(self, bookmark_name, track_id, playlist_id):
        self._controller.config.load_config(open(self._config_file_valid))
        assert (track_id, playlist_id) != self._controller.get_bookmark(bookmark_name)
        self._controller.set_bookmark(bookmark_name, track_id, playlist_id)
        self._reload()
        assert (track_id, playlist_id) == self._controller.get_bookmark(bookmark_name)

    @pytest.mark.parametrize("bookmark_name", (
            "current",
            "alpha",
            "mybookmark"
    ))
    def test_remove_bookmark(self, bookmark_name):
        self._controller.config.load_config(open(self._config_file_valid))

        # Assure the bookmark exist (no exception should be raised)
        track_id, playlist_id = self._controller.get_bookmark(bookmark_name)

        self._controller.clear_bookmark(bookmark_name)
        self._reload()

        with pytest.raises(KeyError):
            track_id, playlist_id = self._controller.get_bookmark(bookmark_name)

    def test_duplicate_save(self):
        self._controller.config.load_config(open(self._config_file_valid))
        with tempfile.TemporaryFile("r+") as outfile:
            self._controller.config.save_config(outfile)
            self._controller.config.save_config(outfile)
            self._controller.config.save_config(outfile)
            self._controller.config.load_config(outfile)
