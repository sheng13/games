import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_FIXTURE = PROJECT_ROOT / "tests" / "fixtures" / "luxfatum-installer.sample"
sys.path.insert(0, str(PROJECT_ROOT))

from app import app


class LuxFatumLobbyTest(unittest.TestCase):
    def setUp(self):
        original_config = app.config.copy()
        self.addCleanup(app.config.update, original_config)
        app.config.update(TESTING=True, LUXFATUM_INSTALLER="")
        self.client = app.test_client()

    def test_lobby_exposes_downloadable_luxfatum_game(self):
        lobby = self.client.get("/")
        try:
            body = lobby.get_data(as_text=True)
            self.assertEqual(lobby.status_code, 200)
            self.assertIn("LuxFatum", body)
            self.assertIn('href="/luxfatum/download"', body)
        finally:
            lobby.close()

    def test_download_without_configuration_returns_not_found(self):
        download = self.client.head("/luxfatum/download")
        try:
            self.assertEqual(download.status_code, 404)
            self.assertNotIn("Content-Disposition", download.headers)
        finally:
            download.close()

    def test_configured_installer_supports_head(self):
        app.config["LUXFATUM_INSTALLER"] = str(INSTALLER_FIXTURE)
        with self.client.head("/luxfatum/download") as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"")
            self.assertIn("attachment", response.headers["Content-Disposition"])
            self.assertIn(INSTALLER_FIXTURE.name, response.headers["Content-Disposition"])
            self.assertEqual(int(response.headers["Content-Length"]),
                             INSTALLER_FIXTURE.stat().st_size)

    def test_configured_installer_returns_fixture_bytes(self):
        app.config["LUXFATUM_INSTALLER"] = str(INSTALLER_FIXTURE)
        with self.client.get("/luxfatum/download") as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, INSTALLER_FIXTURE.read_bytes())

    def test_relative_installer_path_uses_project_root(self):
        app.config["LUXFATUM_INSTALLER"] = str(INSTALLER_FIXTURE.relative_to(PROJECT_ROOT))
        with self.client.head("/luxfatum/download") as response:
            self.assertEqual(response.status_code, 200)

    def test_missing_installer_returns_not_found_without_path_leak(self):
        missing_path = PROJECT_ROOT / "tests" / "fixtures" / "not-present-installer.exe"
        self.assertFalse(missing_path.exists())
        app.config["LUXFATUM_INSTALLER"] = str(missing_path)
        try:
            response = self.client.get("/luxfatum/download")
        except OSError as error:
            self.fail(f"Unavailable installer must return 404, not {type(error).__name__}")
        with response:
            self.assertEqual(response.status_code, 404)
            self.assertNotIn(str(missing_path), response.get_data(as_text=True))

    def test_directory_is_not_downloadable(self):
        app.config["LUXFATUM_INSTALLER"] = str(INSTALLER_FIXTURE.parent)
        try:
            response = self.client.head("/luxfatum/download")
        except OSError as error:
            self.fail(f"Installer directory must return 404, not {type(error).__name__}")
        with response:
            self.assertEqual(response.status_code, 404)

    def test_installer_setting_is_loaded_from_environment(self):
        expected = str(INSTALLER_FIXTURE.relative_to(PROJECT_ROOT))
        environment = {**os.environ, "LUXFATUM_INSTALLER": expected,
                       "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run(
            [sys.executable, "-B", "-c",
             "import json; from app import app; "
             "print(json.dumps(app.config.get('LUXFATUM_INSTALLER')))"],
            cwd=PROJECT_ROOT, env=environment, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), expected)

    def test_installer_is_disabled_by_default(self):
        environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        environment.pop("LUXFATUM_INSTALLER", None)
        result = subprocess.run(
            [sys.executable, "-B", "-c",
             "import json; from app import app; "
             "print(json.dumps(app.config.get('LUXFATUM_INSTALLER')))"],
            cwd=PROJECT_ROOT, env=environment, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), "")

    def test_game_pages_and_browser_dependency_are_available(self):
        for route in ("/", "/guess", "/gomoku", "/tictactoe", "/snake", "/2048",
                      "/chess", "/tetris", "/breakout", "/minesweeper", "/online",
                      "/static/socket.io.min.js"):
            with self.subTest(route=route):
                with self.client.get(route) as response:
                    self.assertEqual(response.status_code, 200)

    def test_guess_game_still_starts(self):
        with self.client.post("/api/new-game", json={"difficulty": "normal"}) as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["maximum"], 100)


if __name__ == "__main__":
    unittest.main()
