import os
import sys
from unittest.mock import patch, MagicMock
import types

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "hass_security_dashboard", "back"))

sys.modules.setdefault("requests", MagicMock())
import types
sys.modules.setdefault("yaml", types.SimpleNamespace(safe_load=lambda data: {}))

# Provide a minimal stub for the flask module so app.py can be imported
class DummyFlask:
    def __init__(self, *args, **kwargs):
        self.static_folder = kwargs.get("static_folder")
    def route(self, *args, **kwargs):
        def decorator(func):
            return func
        return decorator

flask_stub = types.SimpleNamespace(
    Flask=DummyFlask,
    jsonify=lambda *a, **k: None,
    request=MagicMock(),
    send_file=lambda *a, **k: None,
    send_from_directory=lambda *a, **k: None,
)

sys.modules.setdefault("flask", flask_stub)

import importlib
app_module = importlib.import_module("hass_security_dashboard.back.app")


def test_static_folder_path():
    expected = os.path.join(os.path.dirname(app_module.__file__), "..", "front", "assets")
    assert app_module.app.static_folder == expected


def test_index_uses_front_dir():
    with patch.object(app_module, "send_from_directory", return_value="ok") as sfd:
        result = app_module.index()
        sfd.assert_called_once_with(app_module.FRONT_DIR, "index.html")
        assert result == "ok"
