import os
import pytest
from check_mk_web_api.web_api import WebApi

api = WebApi(
    os.environ['CHECK_MK_URL'],
    os.environ['CHECK_MK_USER'],
    os.environ['CHECK_MK_SECRET']
)


class TestSites():

    @pytest.mark.skip(reason="bug in Check_Mk")
    def test_get_site(self):
        assert api.get_site('checkmd2')

    @pytest.mark.skip(reason="bug in Check_Mk")
    def test_set_site(self):

        site_alias = 'alias_green'
        config = api.get_site('checkmd2')['site_config']
        config['alias'] = site_alias

        api.set_site('checkmd2', config)
        assert api.get_site('checkmd2')['site_config']['alias'] == site_alias

    @pytest.mark.skip(reason="bug in Check_Mk")
    def test_login_site(self):
        api.add_user('user00', 'User 00', 'p4ssw0rd')
        api.login_site('cmk', 'user00', 'p4ssw0rd')

    @pytest.mark.skip(reason="bug in Check_Mk")
    def test_logout_site(self):
        api.add_user('user00', 'User 00', 'p4ssw0rd')
        api.login_site('cmk', 'user00', 'p4ssw0rd')
        api.logout_site('cmk')
