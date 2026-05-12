# Agentic Metrics
App to demonstrate create agentic metrics and displaying them.

Pre-requisites:
- [ ] OpenShift 4.10+
- [ ] OpenShift CLI
- [ ] Helm 3
- [ ] envsubst cli
- [ ] Ability to use an S3-compatible object store (S3, Minio, etc.)

## Metric Generator

Take a look at the `README.md` in the `metric-generator` directory.

## Metric Dashboard

Take a look at the `README.md` in the `metric-dashboard` directory.

## Basic Setup
### OpenLIT (Basic)

#### 1. Create deployment
```shell
oc new-project openlit
oc adm policy add-scc-to-user anyuid -z default -n openlit
oc apply -f metric-generator/openshift/helm-repo.yaml
```

#### 2. Use OpenShift Web Console to create helm deployment

#### 3. Create routes
```shell
oc apply -f metric-generator/openshift/openlit-route.yaml
oc apply -f metric-generator/openshift/openlit-otel-route.yaml
# Troubleshooting: 
# if you see missing `NEXTAUTH_SECRET`,
# then connect to the pod and delete `/app/client/data/.nextauth_secret`
```

#### 4. (Optional) Set up Minio
```shell
oc new-project minio
oc apply -f metric-generator/openshift/minio-all.yaml
oc wait --for=condition=complete job/create-minio-buckets --timeout=120s
export S3_ACCESS_KEY=$(oc get secret minio-secret -o jsonpath='{.data.minio_root_user}' | base64 -d)
export S3_SECRET_KEY=$(oc get secret minio-secret -o jsonpath='{.data.minio_root_password}' | base64 -d)
TLS=$(oc get route minio-api -n minio -o jsonpath='{.spec.tls.termination}')                                               
[ -n "$TLS" ] && SCHEME="https" || SCHEME="http"
export S3_ENDPOINT="http://$(oc get service -oname).minio.svc.cluster.local:9000"
export S3_REGION=$(oc get secret minio-secret -o jsonpath='{.data.region}' | base64 -d)
export S3_BUCKET=tempo-traces
envsubst < metric-generator/openshift/storage-secret.yaml.template > metric-generator/openshift/storage-secret.yaml

# Troubleshooting: 
# Run oc logs job/create-minio-buckets -nminio -f
```

#### 5. (Optional) Manually update object store values in metric-generator/openshift/storage-secret.yaml
#### (only required if not using Minio and object store values are different 
#### from auto-populated values in Step 4)

#### 6. Set up Tracing 
```shell
oc new-project observability

oc apply -f metric-generator/openshift/tempo-subscription.yaml
oc apply -f metric-generator/openshift/otel-subscription.yaml
oc apply -f metric-generator/openshift/coo-subscription.yaml

until oc get crd tempostacks.tempo.grafana.com  2>/dev/null; do sleep 5; done
echo "tempostacks.tempo.grafana.com CRD is ready"
until oc get crd opentelemetrycollectors.opentelemetry.io 2>/dev/null; do sleep 5; done
echo "opentelemetrycollectors.opentelemetry.io CRD is ready"
until oc get crd uiplugins.observability.openshift.io 2>/dev/null; do sleep 5; done
echo "uiplugins.observability.openshift.io CRD is ready"

oc apply -f metric-generator/openshift/storage-secret.yaml
oc apply -f metric-generator/openshift/sa.yaml
oc apply -f metric-generator/openshift/tempo-stack.yaml
oc apply -f metric-generator/openshift/otel-collector.yaml
oc apply -f metric-generator/openshift/ui-plugin.yaml
```
