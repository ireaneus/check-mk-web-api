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


class TestFolders():
    def setup(self):
        for folder in api.get_all_folders():
            if folder != '':
                api.delete_folder(folder)

    @filter_uri
    def test_get_folder(self):
        api.add_folder('productive')
        assert api.get_folder('productive')

    @filter_uri
    def test_get_nonexistent_folder(self):
        with pytest.raises(CheckMkWebApiException):
            assert api.get_folder('productive')

    @filter_uri
    def test_get_hosts_by_folder(self):
        api.add_folder('test')
        api.add_host('host00', 'test')
        api.add_host('host01', 'test')

        hosts = api.get_hosts_by_folder('test')
        assert len(hosts) == 2
        assert 'host00' in hosts
        assert 'host01' in hosts

    @filter_uri
    def test_get_all_folders(self):
        api.add_folder('productive')
        api.add_folder('testing')

        folders = api.get_all_folders()
        assert 'productive' in folders
        assert 'testing' in folders

    @filter_uri
    def test_add_folder(self):
        api.add_folder('productive')
        assert 'productive' in api.get_all_folders()

    @filter_uri
    def test_edit_folder(self):
        api.add_folder('productive', snmp_community='public')
        assert api.get_folder('productive')['attributes']['snmp_community'] == 'public'

        api.edit_folder('productive', snmp_community='private')
        assert api.get_folder('productive')['attributes']['snmp_community'] == 'private'

    @filter_uri
    def test_edit_nonexistent_folder(self):
        with pytest.raises(CheckMkWebApiException):
            assert api.edit_folder('productive')

    @filter_uri
    def test_delete_folder(self):
        api.add_folder('productive')
        assert 'productive' in api.get_all_folders()

        api.delete_folder('productive')
        assert 'productive' not in api.get_all_folders()

    @filter_uri
    def test_delete_nonexistent_folder(self):
        with pytest.raises(CheckMkWebApiException):
            api.delete_folder('productive')
