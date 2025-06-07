import tempfile
import json
from unittest.mock import patch, MagicMock
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "hass_security_dashboard", "back"))

sys.modules.setdefault("requests", MagicMock())
import types
sys.modules.setdefault("yaml", types.SimpleNamespace(safe_load=lambda data: {}))

from hass_security_dashboard.back import security_scanner as ss


def test_parse_configuration(tmp_path):
    config = tmp_path / 'configuration.yaml'
    config.write_text('http:\n  ssl_certificate: cert.pem\nmqtt:\n  password: pass')
    with patch('yaml.safe_load', return_value={'http': {'ssl_certificate': 'cert.pem'}, 'mqtt': {'password': 'pass'}}):
        result = ss.parse_configuration(str(config))
    assert result['http_ssl'] is True
    assert result['mqtt_has_password'] is True


def test_parse_configuration_missing_values(tmp_path):
    config = tmp_path / 'configuration.yaml'
    config.write_text('http: {}\nmqtt: {}')
    with patch('yaml.safe_load', return_value={'http': {}, 'mqtt': {}}):
        result = ss.parse_configuration(str(config))
    assert result['http_ssl'] is False
    assert result['mqtt_has_password'] is False


def test_perform_full_scan_aggregates_results():
    with patch.object(ss, 'scan_open_ports', return_value=[22]), \
         patch.object(ss, 'check_ssl_certificate', return_value=10), \
         patch.object(ss, 'check_mqtt_security', return_value=True), \
         patch.object(ss, 'check_cloudflare', return_value=True), \
         patch.object(ss, 'check_duckdns', return_value=True), \
         patch.object(ss, 'parse_configuration', return_value={'http_ssl': True}), \
         patch.object(ss, 'get_ssh_addon_details', return_value={'running': True}), \
         patch.object(ss, 'get_core_info', return_value={'version': '1.0'}):
        results = ss.perform_full_scan('example.com', 'token', 'sub.domain', '/tmp/config')
    assert results['open_ports'] == [22]
    assert results['ssl_days_left'] == 10
    assert results['mqtt_secure'] is True
    assert results['cloudflare_protected'] is True
    assert results['duckdns_match'] is True
    assert results['config_security'] == {'http_ssl': True}
    assert results['ssh_addon'] == {'running': True}
    assert results['core'] == {'version': '1.0'}


def test_check_cloudflare_proxied_true():
    mock_zone_resp = MagicMock()
    mock_zone_resp.json.return_value = {
        'result': [{'id': 'z1', 'name': 'example.com'}]
    }
    mock_dns_resp = MagicMock()
    mock_dns_resp.json.return_value = {
        'result': [{'name': 'sub.example.com', 'proxied': True}]
    }
    with patch('requests.get', side_effect=[mock_zone_resp, mock_dns_resp]):
        assert ss.check_cloudflare('sub.example.com', 'token') is True


def test_check_cloudflare_proxied_false():
    mock_zone_resp = MagicMock()
    mock_zone_resp.json.return_value = {
        'result': [{'id': 'z1', 'name': 'example.com'}]
    }
    mock_dns_resp = MagicMock()
    mock_dns_resp.json.return_value = {
        'result': [{'name': 'sub.example.com', 'proxied': False}]
    }
    with patch('requests.get', side_effect=[mock_zone_resp, mock_dns_resp]):
        assert ss.check_cloudflare('sub.example.com', 'token') is False
