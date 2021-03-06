# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid
from unittest import TestCase

import datetime
import httpretty
from faker import Faker
from polyaxon_schemas.experiment import ExperimentJobStatusConfig, ExperimentJobConfig
from polyaxon_client.jobs import JobClient

faker = Faker()


class TestJobClient(TestCase):
    def setUp(self):
        self.client = JobClient(host='localhost',
                                http_port=8000,
                                ws_port=1337,
                                version='v1',
                                token=faker.uuid4(),
                                reraise=True)

    @httpretty.activate
    def test_get_job(self):
        experiment_uuid = uuid.uuid4().hex
        object = ExperimentJobConfig(uuid=uuid.uuid4().hex,
                                     experiment=experiment_uuid,
                                     created_at=datetime.datetime.now(),
                                     definition={}).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'jobs',
                'uuid'),
            body=json.dumps(object),
            content_type='application/json',
            status=200)
        result = self.client.get_job('username', 'project_name', 1, 'uuid')
        assert object == result.to_dict()

    @httpretty.activate
    def test_get_experiment_job_status(self):
        job_uuid = uuid.uuid4().hex
        object = ExperimentJobStatusConfig(uuid=uuid.uuid4().hex,
                                           job=job_uuid,
                                           created_at=datetime.datetime.now(),
                                           status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'jobs',
                job_uuid,
                'statuses'),
            body=json.dumps({'results': [object], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)
        response = self.client.get_statuses('username', 'project_name', 1, job_uuid)
        assert len(response['results']) == 1
