import os
from tests import filter_uri
import pytest
from check_mk_web_api.exception import CheckMkWebApiException
from check_mk_web_api.web_api import WebApi

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


class TestHostGroup():
    def setup(self):
        api.delete_all_hostgroups()

    @filter_uri
    def test_get_hostgroup(self):
        api.add_hostgroup('vm', 'VM')
        api.get_hostgroup('vm')

    @filter_uri
    def test_get_all_hostgroups(self):
        api.add_hostgroup('vm', 'VM')
        api.add_hostgroup('physical', 'Physical')
        groups = api.get_all_hostgroups()
        assert 'vm' in groups
        assert 'physical' in groups

    @filter_uri
    def test_get_nonexistent_hostgroup(self):
        with pytest.raises(KeyError):
            api.get_hostgroup('vm')

    @filter_uri
    def test_add_hostgroup(self):
        api.add_hostgroup('vm', 'VM')
        assert api.get_hostgroup('vm')['alias'] == 'VM'

    @filter_uri
    def test_add_duplicate_hostgroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.add_hostgroup('vm', 'VM')
            api.add_hostgroup('vm', 'VM')

    @filter_uri
    def test_edit_hostgroup(self):
        api.add_hostgroup('vm', 'VM')
        assert api.get_hostgroup('vm')['alias'] == 'VM'
        api.edit_hostgroup('vm', 'VMs')
        assert api.get_hostgroup('vm')['alias'] == 'VMs'

    @filter_uri
    def test_edit_nonexisting_hostgroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.edit_hostgroup('vm', 'VM')

    @filter_uri
    def test_delete_hostgroup(self):
        api.add_hostgroup('vm', 'VM')
        assert 'vm' in api.get_all_hostgroups()
        api.delete_hostgroup('vm')
        assert 'vm' not in api.get_all_hostgroups()

    @filter_uri
    def test_delete_nonexistent_hostgroup(self):
        with pytest.raises(CheckMkWebApiException):
            api.delete_hostgroup('vm')


