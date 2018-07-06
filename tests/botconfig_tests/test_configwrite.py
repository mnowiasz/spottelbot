import os
import tempfile

import pytest

from spottelbot import botconfig


class TestConfigWrite(object):
    @classmethod
    def setup_class(cls):
        cls._config = botconfig.BotConfig()
        cls._config_path = os.path.dirname(os.path.realpath(__file__))
        cls._config_file_valid = os.path.join(cls._config_path, "valid.config")

    def _reload(self):
        with tempfile.NamedTemporaryFile("r+") as outfile:
            self._config.save_config(outfile.name)
            self._config.load_config(outfile.name)

    def test_writeconfig(self):
        self._config.load_config(self._config_file_valid)
        with tempfile.NamedTemporaryFile("r+") as outfile:
            self._config.save_config(outfile.name)
            self._config.load_config(outfile.name)

    # Altough you can't change the token by commands, it's a good test if the save works - and every
    # config data which can be loaded should be saved, too (even if immutable)
    def test_changetoken(self):
        test_token = "123:45"
        self._config.load_config(self._config_file_valid)
        self._config._telegram_token = test_token
        self._reload()
        assert test_token == self._config._telegram_token

    def test_adduser(self):
        test_id = "4711"
        self._config.load_config(self._config_file_valid)
        self._config.add_access(test_id)
        self._reload()
        assert self._config.has_access(test_id)

    def test_removeuser(self):
        test_id = "543431"
        self._config.load_config(self._config_file_valid)
        self._config.remove_access(test_id)
        self._reload()
        assert not self._config.has_access(test_id)
        assert self._config.has_access("12354")

    # See test_changetoken()
    def test_change_spotify_username(self):
        test_username = "MyNewUsername"
        self._config.load_config(self._config_file_valid)
        self._config._spotify_username = test_username
        self._reload()
        assert test_username == self._config._spotify_username

    # See test_changetoken()
    def test_change_spotify_client_id(self):
        test_client_id = "foobar12345"
        self._config.load_config(self._config_file_valid)
        self._config._spotify_client_id = test_client_id
        self._reload()
        assert test_client_id == self._config._spotify_client_id

    # See test_changetoken()
    def test_change_spotify_client_secret(self):
        test_client_secret = "MyNewSecret"
        self._config.load_config(self._config_file_valid)
        self._config._spotify_client_secret = test_client_secret
        self._reload()
        assert test_client_secret == self._config._spotify_client_secret

    # See test_changetoken()
    def test_change_spotify_redirect_uri(self):
        test_redirect_uri = "http://www.google.com/"
        self._config.load_config(self._config_file_valid)
        self._config._spotify_redirect_uri = test_redirect_uri
        self._reload()
        assert test_redirect_uri == self._config._spotify_redirect_uri

    @pytest.mark.parametrize("bookmark_name, track_id, playlist_id", (
            ("current", "12345abcdef", None),
            ("current", "abcdefg", "hijklmno"),
            ("alpha", "1111111111", None)
    ))
    def test_change_bookmark(self, bookmark_name, track_id, playlist_id):
        self._config.load_config(self._config_file_valid)
        assert (track_id, playlist_id) != self._config.get_bookmark(bookmark_name)
        self._config.set_bookmark(bookmark_name, track_id, playlist_id)
        self._reload()
        assert (track_id, playlist_id) == self._config.get_bookmark(bookmark_name)

    @pytest.mark.parametrize("bookmark_name", (
            "current",
            "alpha",
            "mybookmark"
    ))
    def test_remove_bookmark(self, bookmark_name):
        self._config.load_config(self._config_file_valid)

        # Assure the bookmark exist (no exception should be raised)
        track_id, playlist_id = self._config.get_bookmark(bookmark_name)

        self._config.clear_bookmark(bookmark_name)
        self._reload()

        with pytest.raises(KeyError):
            track_id, playlist_id = self._config.get_bookmark(bookmark_name)

    def test_duplicate_save(self):
        self._config.load_config(self._config_file_valid)
        with tempfile.NamedTemporaryFile("r+") as outfile:
            self._config.save_config(outfile.name)
            self._config.save_config(outfile.name)
            self._config.save_config(outfile.name)
            self._config.load_config(outfile.name)
