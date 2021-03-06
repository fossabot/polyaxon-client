# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.polyaxonfile.logger import logger

from polyaxon_client.base import PolyaxonClient
from polyaxon_schemas.version import (
    CliVersionConfig,
    PlatformVersionConfig,
    LibVersionConfig,
    ChartVersionConfig,
)


class VersionClient(PolyaxonClient):
    """Client to get API version from the server."""
    ENDPOINT = "/versions/"

    def get_cli_version(self):
        request_url = self._build_url(self._get_http_url(), 'cli')
        response = self.get(request_url)
        data_dict = response.json()
        logger.debug("CLI Version info :{}".format(data_dict))
        return CliVersionConfig.from_dict(data_dict)

    def get_platform_version(self):
        request_url = self._build_url(self._get_http_url(), 'platform')
        response = self.get(request_url)
        data_dict = response.json()
        logger.debug("Platform Version info :{}".format(data_dict))
        return PlatformVersionConfig.from_dict(data_dict)

    def get_lib_version(self):
        request_url = self._build_url(self._get_http_url(), 'lib')
        response = self.get(request_url)
        data_dict = response.json()
        logger.debug("Lib Version info :{}".format(data_dict))
        return LibVersionConfig.from_dict(data_dict)

    def get_chart_version(self):
        request_url = self._build_url(self._get_http_url(), 'chart')
        response = self.get(request_url)
        data_dict = response.json()
        logger.debug("Lib Version info :{}".format(data_dict))
        return ChartVersionConfig.from_dict(data_dict)
