# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ProjectConfig, ExperimentGroupConfig

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException


class ProjectClient(PolyaxonClient):
    """Client to get projects from the server"""
    ENDPOINT = "/"

    def list_projects(self, username, page=1):
        request_url = self._build_url(self._get_http_url(), username)
        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ProjectConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving projects')
            return []

    def get_project(self, username, project_name):
        request_url = self._build_url(self._get_http_url(), username, project_name)
        try:
            response = self.get(request_url)
            return ProjectConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving project')
            return None

    def create_project(self, project_config):
        try:
            response = self.post(self._get_http_url('/projects'), json=project_config.to_dict())
            return ProjectConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating project')
            return None

    def update_project(self, username, project_name, patch_dict):
        request_url = self._build_url(self._get_http_url(), username, project_name)
        try:
            response = self.patch(request_url, json=patch_dict)
            return ProjectConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating project')
            return None

    def delete_project(self, username, project_name):
        request_url = self._build_url(self._get_http_url(), username, project_name)
        try:
            response = self.delete(request_url)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting project')
            return None

    def upload_repo(self, username, project_name, files, files_size=None):
        """Uploads code data related for this project from the current dir."""
        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'repo', 'upload')

        try:
            response = self.upload(request_url, files=files, files_size=files_size)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating project repo')
            return None

    def list_experiment_groups(self, username, project_name, page=1):
        """Fetch list of experiment groups related to this project."""
        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'groups')

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentGroupConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment groups')
            return []

    def create_experiment_group(self, username, project_name, experiment_group_config):
        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'groups')

        try:
            response = self.post(request_url, json=experiment_group_config.to_dict())
            return ExperimentGroupConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating experiment group')
            return None

    def list_experiments(self, username, project_name, page=1):
        """Fetch list of experiments related to this project."""
        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'experiments')

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiments')
            return []

    def create_experiment(self, username, project_name, experiment_config):
        request_url = self._build_url(self._get_http_url(), username, project_name, 'experiments')

        try:
            response = self.post(request_url, json=experiment_config.to_dict())
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating experiment group')
            return None

    def clone_repo(self, username, project_name):
        # TODO
        pass

    def create_tensorboard(self, username, project_name):
        # TODO
        pass

    def create_notebook(self, username, project_name):
        # TODO
        pass
