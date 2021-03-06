import os
from tests import filter_uri
import pytest

from check_mk_web_api.web_api_alerts import WebApiAlerts

api = WebApiAlerts(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


class TestAlerts():

    def test_get_alerts_does_not_error(self):
        assert api.get_alerts()

    @pytest.mark.skip('incomplete code')
    @filter_uri
    def test_get_alerts_contains_information(self):
        alert_results = api.get_alerts()
        assert len(alert_results) == 4
        assert alert_results[1] == ['localhost', 'Check_MK Discovery', '1', '0', '0', '1']

    @pytest.mark.skip('currently throwing unknown api action error')
    @filter_uri
    def test_ack_alert(self):
        hostname = "hostname"
        comment = "acknowledge"
        servicename = "serviceName"
        assert api.ack_alerts(hostname, comment, servicename)

    @pytest.mark.skip('incomplete code')
    @filter_uri
    def test_get_alert_stats(self):
        result = api.view_alert_stats()
        expected_result = [[
            'host',
            'service_description',
            'alert_stats_crit',
            'alert_stats_unknown',
            'alert_stats_warn',
            'alert_stats_problem'],
           ['localhost', 'Check_MK Discovery', '1', '0', '0', '1'],
           ['localhost', '', '0', '0', '0', '0'],
           ['localhost', 'PING', '0', '0', '0', '0']]

        assert result == expected_result

    @filter_uri
    def test_get_alert_handler_executions(self):
        result = api.alert_handler_executions()
        expected_result = [[
            'log_icon',
            'log_time',
            'log_command',
            'log_type',
            'host',
            'service_description',
            'log_state',
            'log_plugin_output']]

        assert result == expected_result

