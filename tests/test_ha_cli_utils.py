import json
import subprocess
from unittest.mock import patch, MagicMock
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "hass_security_dashboard", "back"))

import pytest

from hass_security_dashboard.back import ha_cli_utils


def test_run_ha_command_success():
    mock_completed = subprocess.CompletedProcess(['ha'], 0, stdout='ok')
    with patch('subprocess.run', return_value=mock_completed) as run:
        out = ha_cli_utils.run_ha_command(['core', 'info'])
        run.assert_called_once()
        assert out == 'ok'


def test_run_ha_command_not_found():
    with patch('subprocess.run', side_effect=FileNotFoundError):
        with pytest.raises(ha_cli_utils.HACliUnavailable):
            ha_cli_utils.run_ha_command(['core', 'info'])


def test_run_ha_command_calledprocesserror():
    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'ha')):
        assert ha_cli_utils.run_ha_command(['core', 'info']) is None


def test_get_addon_info_success():
    data = {'version': '1.0', 'update_available': False, 'state': 'started'}
    with patch('hass_security_dashboard.back.ha_cli_utils.run_ha_command', return_value=json.dumps(data)):
        info = ha_cli_utils.get_addon_info('core_ssh')
        assert info['version'] == '1.0'
        assert info['update_available'] is False
        assert info['state'] == 'started'


def test_get_core_info_success():
    payload = {'version': '1.0', 'version_latest': '1.1'}
    with patch('hass_security_dashboard.back.ha_cli_utils.run_ha_command', return_value=json.dumps(payload)):
        info = ha_cli_utils.get_core_info()
        assert info['version'] == '1.0'
        assert info['update_available'] is True
