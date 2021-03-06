# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.experiment import (
    ExperimentJobStatusConfig,
    ExperimentJobConfig,
)

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException


class JobClient(PolyaxonClient):
    """Client to get jobs from the server"""
    ENDPOINT = "/"

    def get_job(self, username, project_name, experiment_sequence, job_uuid):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'jobs',
                                      job_uuid)
        try:
            response = self.get(request_url)
            return ExperimentJobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving job')
            return None

    def get_statuses(self, username, project_name, experiment_sequence, job_uuid, page=1):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'jobs',
                                      job_uuid,
                                      'statuses')

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentJobStatusConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving job statuses')
            return []

    def resources(self, username, project_name, experiment_sequence, job_uuid,
                  message_handler=None):
        """Streams job resources using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'jobs',
                                      job_uuid,
                                      'resources')
        self.socket(request_url, message_handler=message_handler)

    def logs(self, username, project_name, experiment_sequence, job_uuid, message_handler=None):
        """Streams job logs using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'jobs',
                                      job_uuid,
                                      'logs')
        self.socket(request_url, message_handler=message_handler)
