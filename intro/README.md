# Lab Exercise for Introduction to Kubernetes with IGNW

## Overview
This lab will walk you through deploying an application to your Kubernetes cluster using the kubectl command line and pre-made Kubernetes manifests. We intentionally do a broken deployment, we'll be fixing that as part of the lab.

Pre-reqs:
- A working k8s cluster
- Clone the repo `git clone https://github.com/IGNW/k8s-workshop.git`
- `cd` to the `intro` directory in the repo: `cd intro`

### Deploy Redis Key/Value Store
Steps:
- Deploy a dedicated Namespace for Redis and our frontend application
- Deploy a single redis instance to the new namespace
- Inspect the objects we've deployed via kubectl and the dashboard

1. Create namespace in Kubernetes
    * `kubectl apply -f namespace.yml`
      Deploy the namespace defined in the file 'namespace.yml'. This is the namespace referenced in our other manifests.

2. Deploy Redis Server
    * `kubectl apply -f redis/`
      Deploy all '.yml' files in the 'redis' directory
    * `kubectl get deployments`
      List all deployment resources in the default namespace.  Notice this does not return anything as we deployed into the `k8s-workshop` namespace
    * `kubectl get pods`
      List all pod resources in the default namespace.  Notice this also does not return anything.
    * `kubectl get --namespace k8s-workshop deployments,pods`
      Lists the deployment and pod resouces, but now scope the request to the `k8s-workshop` namespace.
    * `kubectl describe --namespace k8s-workshop pod <pod>`
      Describe the details of a specific pod, you will have to copy/paste the name of the pod in place of <pod>
    * `kubectl get --namespace k8s-workshop services`
      Show all services in the k8s-workshop namespace, notice that our redis instance is fronted by a name

You should now see a single redis server deployed in the k8s-workshop namespace along with a service for redis.

### Deploy Frontend Application
Steps:
- Deploy our python app to the default namespace
- Expose our application via a cloud load balancer
- Access our app via the cloud load balancer with curl or a browser
- Troubleshoot the resulting failure
- Patch the deployment and observe the rolling update
- Verify we have fixed out application

1. Deploy the frontend application
    * `kubectl apply -f frontend/`
      This creates the deployment and service objects for our application
    * `kubectl get pods`
      Lists all pods for our newly created deployment
    * `kubectl get services`
      Inspect the newly created load balancer
    
1. Test
    * `curl [external_ip]`
      This will return the name of the pod that is responding
    * `curl [external_ip]/foo/bar`
      This _should_ store the value `bar` in the key `foo` on our redis instance, but it will fail
    * `kubectl logs <frontend pod name>`
      This will show us the logs for our frontend application, we should be able to see a Redis timeout in the logs

1. Fix the broken deployment
    * `kubectl delete -f frontend/`
    * `kubectl apply -f frontend/frontend.deployment.yml --namespace k8s-workshop`
      `kubectl apply -f frontend/frontend.service.yml --namespace k8s-workshop`
      This will delete and re-apply our frontend application into the correct `k8s-workshop` namespace
    * `watch kubectl get services --namespace k8s-workshop`
      This will list the new service endpoint we just created, we'll wait for the new IP to show up so we can test
1. Test
    * `curl [external_ip]/foo/bar`
      You can now see the service is functioning as expected
    * `curl [external_ip]/foo`
      We can also query the value from the database.

### Scaling the aplication
1. Scale the Deployment
    * `kubectl --namespace k8s-workshop scale deployment frontend --replicas=2`
      This will tell Kubernetes to increase the number of copies of `frontend` to 2
    * `kubectl --namespace k8s-workshop get pods`
      List the currently deployed pods, notice how there are now 4 copies of `frontend`
    * `curl [external_ip]`
      Do this several times in a row, see how the pod name changes?

1. Use a Horizontal Pod Autoscaler to automate the process
    * `kubectl get hpa --namespace k8s-workshop`
      Inspect the HPA we created earlier
    * Install `ab`: `sudo apt-get install apache2-utils --yes`
    * Apply some load `ab -n 30000 -c 100 http://[external_ip]:[port]/load`
    * `kubectl get hpa --namespace k8s-workshop`
      Show the status of the HPA we just triggered
    * `kubectl get pods --namespace k8s-workshop`
      Show the increased number of pods in the cluster
    * Wait for the `ab` run to finish
    * `kubectl get hpa,pods --namespace k8s-workshop`
      Inspect the HPA and pods to see that the HPA has scaled back down, this may take a few minutes as we have to wait for the HPA cooldown timer to expire

