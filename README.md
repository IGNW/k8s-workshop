# IGNW Kubernetes Workshop Supporting Material

This repository contains the code and documentation used by IGNW for Kubenetes training.

* [Kube 101 Walkthrough](kube_101/README.md)

In our workshops, we utilize a simple 2 tier demo application. The "frontend" app is a simple flask app (see below) that interacts with a redis key-value store. More advanced workshops utilize a microservices demo application with multiple n-tier services.

* [Demo Application](app/README.md)

### Interacting with the application:
* [service_ip]:[port]/[key]/[value] will set a value
* [service_ip]:[port]/[key] will retrieve the key
* [service_ip]:[port] returns "Hello from k8s: <podname>"

* [service_ip]:[port]/healthz returns a HTTP 200 with "alive"
* [service_ip]:[port]/nhealthz returns a HTTP 500

* [service_ip]:[port]/load will cause the app to generate high CPU load for 5 seconds

### Optional Configuration
* When the environment variable `CHAOS` is set to `true` then the app will terminate after a random number of requests between 1 and 100.
