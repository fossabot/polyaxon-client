# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid
from unittest import TestCase
import httpretty
from faker import Faker
from polyaxon_schemas.experiment import ExperimentConfig

from polyaxon_schemas.project import ProjectConfig, ExperimentGroupConfig

from polyaxon_client.project import ProjectClient

faker = Faker()


class TestProjectClient(TestCase):
    def setUp(self):
        self.client = ProjectClient(host='localhost',
                                    http_port=8000,
                                    ws_port=1337,
                                    version='v1',
                                    token=faker.uuid4(),
                                    reraise=True)

    @httpretty.activate
    def test_list_projects(self):
        projects = [ProjectConfig(faker.word).to_dict() for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user'
            ),
            body=json.dumps({'results': projects, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_projects('user')
        assert len(response['results']) == 10
        assert response['count'] == 10
        assert response['next'] is None
        assert response['previous'] is None

    @httpretty.activate
    def test_get_project(self):
        object = ProjectConfig(faker.word()).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project'),
            body=json.dumps(object),
            content_type='application/json',
            status=200)
        result = self.client.get_project('user', 'project')
        assert object == result.to_dict()

    @httpretty.activate
    def test_create_project(self):
        object = ProjectConfig(faker.word())
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                'projects'),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_project(object)
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_update_project(self):
        object = ProjectConfig(faker.word())
        httpretty.register_uri(
            httpretty.PATCH,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project'),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_project('user', 'project', {'name': 'new'})
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_delete_project(self):
        project_uuid = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.DELETE,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project'),
            content_type='application/json',
            status=204)
        result = self.client.delete_project('user', 'project')
        assert result.status_code == 204

    @httpretty.activate
    def test_upload_repo(self):
        httpretty.register_uri(
            httpretty.PUT,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'repo',
                'upload'),
            content_type='application/json',
            status=204)
        files = [('code', ('repo',
                           open('./tests/fixtures_static/repo.tar.gz', 'rb'),
                           'text/plain'))]
        result = self.client.upload_repo('user', 'project', files=files, files_size=10)
        assert result.status_code == 204

    @httpretty.activate
    def test_list_experiment_groups(self):
        project_uuid = uuid.uuid4().hex
        experiment_groups = [
            ExperimentGroupConfig(content=faker.word, project=project_uuid).to_dict()
            for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'groups'),
            body=json.dumps({'results': experiment_groups, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiment_groups('user', 'project')
        assert len(response['results']) == 10

    @httpretty.activate
    def test_create_experiment_group(self):
        project_uuid = uuid.uuid4().hex
        object = ExperimentGroupConfig(content=faker.word(), project=project_uuid)
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'groups'),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_experiment_group('user', 'project', object)
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_list_experiments(self):
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [ExperimentConfig(config={}, uuid=xp_uuid, project=project_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'experiments'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('user', 'project')
        assert len(response['results']) == 10

        # pagination

        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'experiments') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('user', 'project', page=2)
        assert len(response['results']) == 10

    @httpretty.activate
    def test_create_experiment(self):
        project_uuid = uuid.uuid4().hex
        object = ExperimentConfig(project=project_uuid, config={})
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'experiments'),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_experiment('user', 'project', object)
        assert result.to_dict() == object.to_dict()
