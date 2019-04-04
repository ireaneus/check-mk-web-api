import os
import pytest
from check_mk_web_api.exception import CheckMkWebApiException
from check_mk_web_api.web_api import WebApi

from tests import my_workingvcr
from functools import wraps

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


class TestServiceGroup():
    # @my_workingvcr
    def setup(self):
        api.delete_all_servicegroups()

    @my_workingvcr
    def test_get_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert api.get_servicegroup('db')

    @my_workingvcr
    def test_get_all_servicegroups(self):
        api.add_servicegroup('db', 'Database')
        api.add_servicegroup('web', 'Webserver')
        groups = api.get_all_servicegroups()
        assert 'db' in groups
        assert 'web' in groups

    @my_workingvcr
    def test_get_nonexistent_servicegroup(self):
        with pytest.raises(KeyError):
            api.get_servicegroup('db')

    @my_workingvcr
    def test_add_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert api.get_servicegroup('db')['alias'] == 'Database'

    @my_workingvcr
    def test_add_duplicate_servicegroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.add_servicegroup('db', 'Database')
            api.add_servicegroup('db', 'Database')

    @my_workingvcr
    def test_edit_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert api.get_servicegroup('db')['alias'] == 'Database'
        api.edit_servicegroup('db', 'Databases')
        assert api.get_servicegroup('db')['alias'] == 'Databases'

    @my_workingvcr
    def test_edit_nonexisting_servicegroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.edit_servicegroup('db', 'Database')

    @my_workingvcr
    def test_delete_servicegroup(self):
        api.add_servicegroup('db', 'Database')
        assert 'db' in api.get_all_servicegroups()
        api.delete_servicegroup('db')
        assert 'db' not in api.get_all_servicegroups()

    @my_workingvcr
    def test_delete_nonexistent_servicegroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.delete_servicegroup('db')

    @my_workingvcr
    def test_all_services(self):
        expected_result = [['service_state',
                            'service_description',
                            'service_icons',
                            'svc_plugin_output',
                            'svc_state_age',
                            'svc_check_age',
                            'perfometer'],
                           ['WARN',
                            'Check_MK',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp ack '
                            'comment',
                            'WARN - [agent] Version: 1.5.0p13, OS: linux, Missing agent sections: '
                            'jolokia_metrics, execution time 0.1 sec',
                            '47 h',
                            '6.98 s',
                            '104 ms'],
                           ['WARN',
                            'Check_MK Discovery',
                            'themes/facelift/images/icon_menu',
                            'WARN - 2 unmonitored services (ntp.time:1, omd_status:1)WARN, no vanished '
                            'services found',
                            '47 h',
                            '71 m',
                            ''],
                           ['OK',
                            'CPU load',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - 15 min load 0.00',
                            '47 h',
                            '6.98 s',
                            '0'],
                           ['OK',
                            'CPU utilization',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - user: 1.6%, system: 0.7%, wait: 0.0%, steal: 0.0%, guest: 0.0%, total: '
                            '2.3%',
                            '47 h',
                            '6.98 s',
                            '2.3%'],
                           ['OK',
                            'Disk IO SUMMARY',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - Utilization: 0.2%, Read: 0.00 B/s, Write: 23.27 kB/s, Average Wait: '
                            '2.83 ms, Average Read Wait: 0.00 ms, Average Write Wait: 2.83 ms, Latency: '
                            '0.60 ms, Average Queue Length: 0.00',
                            '47 h',
                            '6.98 s',
                            '0 B/s / 23.27 kB/s'],
                           ['OK',
                            'Filesystem /',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - 30.3% used (2.96 of 9.78 GB), trend: +21.16 MB / 24 hours',
                            '47 h',
                            '6.99 s',
                            '30.3%'],
                           ['OK',
                            'Interface 2',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - [eth0] (up) MAC: 42:01:0A:8E:00:06, speed unknown, in: 67.85 B/s, out: '
                            '246.08 B/s',
                            '47 h',
                            '6.99 s',
                            '67.8B/s   246.1B/s'],
                           ['PEND',
                            'JVM jvm Uptime',
                            'themes/facelift/images/icon_menu stale',
                            '',
                            '-',
                            '-',
                            ''],
                           ['OK',
                            'Kernel Context Switches',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - 81/s',
                            '47 h',
                            '6.99 s',
                            '81.38/s'],
                           ['OK',
                            'Kernel Major Page Faults',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - 0/s',
                            '47 h',
                            '6.99 s',
                            '0/s'],
                           ['OK',
                            'Kernel Process Creations',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - 4/s',
                            '47 h',
                            '6.99 s',
                            '3.87/s'],
                           ['OK',
                            'Memory',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - RAM used: 299.79 MB of 3.62 GB (8.1%),',
                            '47 h',
                            '6.99 s',
                            '8.1%'],
                           ['OK',
                            'Mount options of /',
                            'themes/facelift/images/icon_menu',
                            'OK - Mount options exactly as expected',
                            '47 h',
                            '7.00 s',
                            ''],
                           ['OK',
                            'Number of threads',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - 116 threads',
                            '47 h',
                            '7.00 s',
                            '116'],
                           ['OK',
                            'OMD checkmd2 apache',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - 0.07 Requests/s, 0.00 Seconds serving/s, 903.58 B Sent/s',
                            '47 h',
                            '7.00 s',
                            ''],
                           ['OK',
                            'OMD checkmd2 Event Console',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - Current events: 0, Virtual memory: 194.93 MB, Overall event limit '
                            'inactive, No hosts event limit active, No rules event limit active, '
                            'Received messages: 0.00/s, Rule hits: 0.00/s, Rule tries: 0.00/s, Message '
                            'drops: 0.00/s, Created events: 0.00/s, Client connects: 0.03/s, Rule hit '
                            'ratio: -, Processing time per message: -, Time per client request: 1.27 ms',
                            '47 h',
                            '7.00 s',
                            ''],
                           ['OK',
                            'OMD checkmd2 performance',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - Host Checks: 0.0/s, Service Checks: 0.3/s, Process Creations: 0.0/s, '
                            'Livestatus Connects: 0.0/s, Livestatus Requests: 0.2/s, Log Messages: '
                            '0.0/s, 1 Hosts, 21 Services, Core version: 3.5.0, Livestatus version: '
                            '1.5.0p13',
                            '47 h',
                            '7.00 s',
                            '0.02/s / 0.32/s'],
                           ['OK',
                            'OMD site apache',
                            'themes/facelift/images/icon_menu',
                            'OK - No activity since last check',
                            '47 h',
                            '7.01 s',
                            ''],
                           ['CRIT',
                            'OMD site status',
                            'themes/facelift/images/icon_menu',
                            'CRIT - stoppedCRIT',
                            '47 h',
                            '7.01 s',
                            ''],
                           ['OK',
                            'TCP Connections',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - ESTABLISHED: 5, CLOSE_WAIT: 1, TIME_WAIT: 8, LISTEN: 7',
                            '47 h',
                            '7.01 s',
                            ''],
                           ['OK',
                            'Uptime',
                            'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
                            'OK - Up since Tue Apr  2 14:51:19 2019 (2d 02:57:58)',
                            '47 h',
                            '7.01 s',
                            '2.1 d']]
        result = api.get_all_services()
        assert result == expected_result
