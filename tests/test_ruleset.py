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


class TestRuleset():

    @filter_uri
    def test_get_ruleset(self):
        assert api.get_ruleset('checkgroup_parameters:hw_fans_perc')

    @filter_uri
    def test_get_nonexistent_rulesets(self):
        with pytest.raises(CheckMkWebApiException):
            api.get_ruleset('nonexistent')

    @filter_uri
    def test_set_nonexistent_rulesets(self):
        with pytest.raises(CheckMkWebApiException):
            api.set_ruleset('nonexistent', {})

    @filter_uri
    def test_get_rulesets(self):
        assert api.get_rulesets()
