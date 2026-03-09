Docker infrastructure (monitoring)
==================================

This folder contains a small monitoring stack used by OsmoWeb:

-  Prometheus (+ Pushgateway + Alertmanager)
-  InfluxDB 2.x
-  Grafana (with provisioning for datasources and dashboards)

The stack is started via simple scripts that run ``docker compose`` in each subfolder.

Quick start
-----------

From the repository root:

.. code:: bash

   cd docker
   ./start_stats.sh

Stop everything:

.. code:: bash

   cd docker
   ./stop_stats.sh

What is started
---------------

.. _prometheus--pushgateway--alertmanager:

Prometheus / Pushgateway / Alertmanager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Location: ``docker/prometheus/``

Started by: ``docker compose -f docker-compose.yml up -d``

Services and ports:

-  Prometheus: ``http://localhost:9090``
-  Pushgateway: ``http://localhost:9091``
-  Alertmanager: ``http://localhost:9093``

Prometheus config:

-  ``docker/prometheus/prometheus.yml``

   -  ``scrape_interval: 1s`` and ``evaluation_interval: 1s``
   -  scrapes Pushgateway multiple times under different ``job_name``\ s (``osmo-*``).

Alerting:

-  ``docker/prometheus/alertmanager.yml`` (email receiver template; placeholders must be replaced for real use)
-  Alert rules are split by network element:

   -  ``docker/prometheus/alerts-bsc.yml``
   -  ``docker/prometheus/alerts-hlr.yml``
   -  ``docker/prometheus/alerts-mgw.yml``
   -  ``docker/prometheus/alerts-msc.yml``
   -  ``docker/prometheus/alerts-stp.yml``

Persistence:

-  ``prometheus-data``, ``pushgateway-data``, ``alertmanager-data`` Docker volumes.

InfluxDB
~~~~~~~~

Location: ``docker/influxdb/``

Service and port:

-  InfluxDB: ``http://localhost:8086``

Initialization:

-  On first start, InfluxDB is initialized via environment variables in ``docker/influxdb/docker-compose.yml``.
-  You almost certainly want to change these defaults before sharing the setup:

   -  ``DOCKER_INFLUXDB_INIT_USERNAME``
   -  ``DOCKER_INFLUXDB_INIT_PASSWORD``
   -  ``DOCKER_INFLUXDB_INIT_ORG``
   -  ``DOCKER_INFLUXDB_INIT_BUCKET``
   -  ``DOCKER_INFLUXDB_INIT_ADMIN_TOKEN``

Persistence:

-  ``influxdb-data`` Docker volume.

Grafana
~~~~~~~

Location: ``docker/grafana/``

Service:

-  Grafana: ``http://localhost:3000``

Important note about networking:

-  Grafana is started with ``network_mode: host``.
-  In this mode, datasource URLs must point to ``localhost`` (not Docker container names), because Docker DNS is not available.

Provisioning:

-  Datasources: ``docker/grafana/provisioning/datasources/datasource.yml``

   -  Prometheus: ``http://localhost:9090``
   -  InfluxDB: ``http://localhost:8086`` (plus org/bucket/token placeholders)

-  Dashboards provider: ``docker/grafana/provisioning/dashboards/dashboards.yml``
-  Dashboards JSON:

   -  ``docker/grafana/provisioning/dashboards/osmo-*.json``

Credentials:

-  Default login is ``admin`` / ``admin`` (see ``docker/grafana/docker-compose.yml``).

Persistence:

-  ``grafana-data`` Docker volume.

.. _notes--common-tweaks:

Notes / common tweaks
---------------------

-  For production-like setups:

   -  You can increase ``scrape_interval`` / ``evaluation_interval`` (1s is very aggressive).
   -  Replace Alertmanager email placeholders with real SMTP settings.
   -  Replace InfluxDB init credentials/token.

-  If you want Grafana in a non-host network mode:

   -  remove ``network_mode: host``
   -  publish ports (``3000:3000``)
   -  attach Grafana to the same Docker network as Prometheus/InfluxDB and update datasource URLs accordingly.
