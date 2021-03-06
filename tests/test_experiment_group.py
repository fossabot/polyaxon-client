# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid
from unittest import TestCase
import httpretty
from faker import Faker

from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ExperimentGroupConfig

from polyaxon_client.experiment_group import ExperimentGroupClient

faker = Faker()


class TestExperimentGroupClient(TestCase):
    def setUp(self):
        self.client = ExperimentGroupClient(host='localhost',
                                            http_port=8000,
                                            ws_port=1337,
                                            version='v1',
                                            token=faker.uuid4(),
                                            reraise=True)

    @httpretty.activate
    def test_get_experiment_group(self):
        object = ExperimentGroupConfig(content=faker.word(),
                                       uuid=uuid.uuid4().hex,
                                       project=uuid.uuid4().hex).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1),
            body=json.dumps(object),
            content_type='application/json',
            status=200)
        result = self.client.get_experiment_group('username', 'project_name', 1)
        assert object == result.to_dict()

    @httpretty.activate
    def test_list_experiments(self):
        group_uuid = uuid.uuid4().hex
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [ExperimentConfig(uuid=xp_uuid,
                                config={},
                                project=project_uuid,
                                group=group_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1,
                'experiments'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('username', 'project_name', 1)
        assert len(response['results']) == 10
        assert response['count'] == 10
        assert response['next'] is None
        assert response['previous'] is None

        # pagination

        httpretty.register_uri(
            httpretty.GET,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1,
                'experiments') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('username', 'project_name', 1, page=2)
        assert len(response['results']) == 10

    @httpretty.activate
    def test_update_experiment_group(self):
        object = ExperimentGroupConfig(content=faker.word(),
                                       uuid=uuid.uuid4().hex,
                                       project=uuid.uuid4().hex)
        httpretty.register_uri(
            httpretty.PATCH,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_experiment_group(
            'username', 'project_name', 1, {'content': 'new'})
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_delete_experiment_group(self):
        httpretty.register_uri(
            httpretty.DELETE,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1),
            content_type='application/json',
            status=204)
        result = self.client.delete_experiment_group( 'username', 'project_name', 1)
        assert result.status_code == 204
