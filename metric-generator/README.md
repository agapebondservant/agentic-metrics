# Metric Generator

App to demonstrate create agentic metrics.

## Environment

### OpenLIT

```shell
# create deployment
oc new-project openlit
oc adm policy add-scc-to-user anyuid -z default -n openlit
oc apply -f ./openshift/helm-repo.yaml
# use OpenShift Web Console to create helm deployment

# create routes
oc apply -f ./openshift/openlit-route.yaml
oc apply -f ./openshift/openlit-otel-route.yaml

# troubleshooting, if you see missing `NEXTAUTH_SECRET`,
#   then connect to the pod and delete `/app/client/data/.nextauth_secret`
```

### OpenShift Telemetry

1. Install the [Logging Operator](https://docs.redhat.com/en/documentation/red_hat_openshift_logging/6.5/html/installing_logging/installing-logging)

2. Install the [Cluster Observability Operator](https://docs.redhat.com/en/documentation/red_hat_openshift_cluster_observability_operator/1-latest/html/installing_red_hat_openshift_cluster_observability_operator/installing-cluster-observability-operators)

3. Install [end to end observability](https://docs.redhat.com/en/documentation/red_hat_openshift_cluster_observability_operator/1-latest/html/installing_red_hat_openshift_cluster_observability_operator/installing-end-to-end-observability) but make sure `tracing: false` as we will configure that by hand

4. Install all [UI plugins](https://docs.redhat.com/en/documentation/red_hat_openshift_cluster_observability_operator/1-latest/html/ui_plugins_for_red_hat_openshift_cluster_observability_operator/index)

5. Do these steps:

    ```shell
    oc new-project observability

    # TODO: update secrets before applying
    oc apply -f ./openshift/storage-secret.yaml

    # service account for the right permissions
    oc apply -f ./openshift/sa.yaml

    # create tempo stack for tracing in openshift
    oc apply -f ./openshift/tempo-stack.yaml
    # might be installed, but just in case its not
    oc apply -f ./openshift/ui-plugin.yaml

    # otel
    oc apply -f ./otel-collector.yaml
    ```

## Setup

```shell
uv python pin 3.11
uv sync
```

Create an `.env` file with the following (replace with real values):

```shell
CREWAI_TRACING_ENABLED=false
OTEL_EXPORTER_OTLP_ENDPOINT="http://your-otel-endpoint.com"
LLM_API_KEY="sk-your-key-here"
LLM_BASE_URL="https://litellm-prod.apps.maas.redhatworkshops.io/v1/"
LLM_MODEL_NAME="model-name"
```

## Run

```shell
uv run --env-file .env ./main.py
```

## Lint

```shell
uv black ./main.py
```

## Docs

1. [OpenShift Setup Blog](https://blog.stderr.at/openshift-platform/observability/observability/2025-11-23-hitchhikers-guide-to-distributed-tracing-with-opentelemetry-and-tempostack-part1/)
2. [GitHub for Blog above](https://github.com/tjungbauer/openshift-clusterconfig-gitops/tree/main/clusters/management-cluster/setup-tempo-operator)
3. [OpenLIT Docs](https://docs.openlit.io/latest/sdk/destinations/openlit#environment-variables)
4. [Crew AI Docs](https://docs.crewai.com/en/observability/openlit)
5. [OpenLIT Helm Chart GitHub](https://github.com/openlit/helm/tree/main/charts/openlit)
6. [How to deploy the new Grafana Tempo operator on OpenShift](https://developers.redhat.com/articles/2023/08/01/how-deploy-new-grafana-tempo-operator-openshift)
7. [Get started with the OpenShift Cluster Observability Operator](https://developers.redhat.com/articles/2024/07/09/get-started-openshift-cluster-observability-operator?source=sso)
8. [Distributed tracing for agentic workflows with OpenTelemetry](https://developers.redhat.com/articles/2026/04/06/distributed-tracing-agentic-workflows-opentelemetry)
