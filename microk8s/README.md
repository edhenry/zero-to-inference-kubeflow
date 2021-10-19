# Microk8s installation

[Microk8s](http://microk8s.io) is a light(er) weight local installation of Kubernetes that can be used as a local dev/test environment for exploring or developing Kubernetes applications. We will be utilizing microk8s for deploying an installation of Kubeflow to use for our local development environment.

Kubeflow and the manifests we'll be using the deploy the solution have only been tested with Kubernetes 1.17 [according to the documentation found in the manifests repository](https://github.com/kubeflow/manifests/tree/v1.3-branch#installation), however we will be installing it on Kubernetes 1.19 and it functions without issue.

We can follow [these directions](https://ubuntu.com/tutorials/install-a-local-kubernetes-with-microk8s#1-overview) from Canonical for installing an instance of microk8s in our Ubuntu environment. I will provide a summary overview of the commands required to deploy below. Please see the link above for more information.

1. Install Microk8s with Kubernetes version 1.19
    ```bash
    $ sudo snap install microk8s --classic --channel=1.19/stable
    ```
    a. Before proceeding, please ensure the initial pods are active by issueing the `microk8s.kubectl get pods -A` command. Your output should look similar to what is shown below : 

    ```bash
        NAMESPACE     NAME                                      READY   STATUS    RESTARTS   AGE
        kube-system   calico-node-mhrc6                         1/1     Running   0          63s
        kube-system   calico-kube-controllers-847c8c99d-z9xjm   1/1     Running   0          63s
    ```
    
    Once these pods are functional proceed to the next step.

2. Enable supporting services DNS, Dashboard, Storage, and GPU (if available)
    ```bash
    $ microk8s enable dns dashboard storage
    ```

    a. Similar to enabling microk8s and watching for pods to have a `Running` status, we'll want to do the same for our `dns`, `dashboard`, and `storage` pods, as well.

    Issue the `microk8s.kubectl get pods -A` command and your output should look similar to what is shown below :

    ```bash
    NAMESPACE     NAME                                         READY   STATUS    RESTARTS   AGE
    kube-system   calico-kube-controllers-847c8c99d-z9xjm      1/1     Running   0          4m17s
    kube-system   metrics-server-8bbfb4bdb-kdrv5               1/1     Running   0          90s
    kube-system   dashboard-metrics-scraper-6c4568dc68-wp88k   1/1     Running   0          85s
    kube-system   coredns-86f78bb79c-mpt62                     1/1     Running   0          98s
    kube-system   calico-node-mhrc6                            1/1     Running   0          4m17s
    kube-system   kubernetes-dashboard-7ffd448895-qc4dq        1/1     Running   0          85s
    kube-system   hostpath-provisioner-5c65fbdb4f-xdhkr        1/1     Running   0          83s
    ```

    Once these pods are all `Running`, we can proceed to the next step of modifying our `kube-apiserver` config.

3. Update kube-apiserver flags

    Append the following to `/var/snap/microk8s/current/args/kube-apiserver`

    ```bash
    --service-account-signing-key-file=${SNAP_DATA}/certs/serviceaccount.key
    --service-account-issuer=kubernetes.default.svc
    ```

4. Restart microk8s
    ```bash
    microk8s stop
    microk8s start
    ```

Once microk8s has started, we can verify that the cluster is operational by checking the `status` and `inspect`ing the microk8s installation.

5. Check that microk8s is operational by issuing the `microk8s status` command. Your output should look similar to what is shown below
    ```bash
    microk8s is running
    high-availability: no
    datastore master nodes: 127.0.0.1:19001
    datastore standby nodes: none
    addons:
    enabled:
        dashboard            # The Kubernetes dashboard
        dns                  # CoreDNS
        ha-cluster           # Configure high availability on the current node
        metrics-server       # K8s Metrics Server for API access to service metrics
        storage              # Storage class; allocates storage from host directory
    disabled:
        ambassador           # Ambassador API Gateway and Ingress
        cilium               # SDN, fast with full network policy
        fluentd              # Elasticsearch-Fluentd-Kibana logging and monitoring
        gpu                  # Automatic enablement of Nvidia CUDA
        helm                 # Helm 2 - the package manager for Kubernetes
        helm3                # Helm 3 - Kubernetes package manager
        host-access          # Allow Pods connecting to Host services smoothly
        ingress              # Ingress controller for external access
        istio                # Core Istio service mesh services
        jaeger               # Kubernetes Jaeger operator with its simple config
        knative              # The Knative framework on Kubernetes.
        kubeflow             # Kubeflow for easy ML deployments
        linkerd              # Linkerd is a service mesh for Kubernetes and other frameworks
        metallb              # Loadbalancer for your Kubernetes cluster
        multus               # Multus CNI enables attaching multiple network interfaces to pods
        prometheus           # Prometheus operator for monitoring and logging
        rbac                 # Role-Based Access Control for authorisation
        registry             # Private image registry exposed on localhost:32000
    ```

6. We can also use the `microk8s inspect` command to view more information about the status of microk8s. Your output should look similar to what is shown below

    ```bash
    Inspecting Certificates
    Inspecting services
    Service snap.microk8s.daemon-cluster-agent is running
    Service snap.microk8s.daemon-containerd is running
    Service snap.microk8s.daemon-apiserver is running
    Service snap.microk8s.daemon-apiserver-kicker is running
    Service snap.microk8s.daemon-control-plane-kicker is running
    Service snap.microk8s.daemon-proxy is running
    Service snap.microk8s.daemon-kubelet is running
    Service snap.microk8s.daemon-scheduler is running
    Service snap.microk8s.daemon-controller-manager is running
    Copy service arguments to the final report tarball
    Inspecting AppArmor configuration
    Gathering system information
    Copy processes list to the final report tarball
    Copy snap list to the final report tarball
    Copy VM name (or none) to the final report tarball
    Copy disk usage information to the final report tarball
    Copy memory usage information to the final report tarball
    Copy server uptime to the final report tarball
    Copy current linux distribution to the final report tarball
    Copy openSSL information to the final report tarball
    Copy network configuration to the final report tarball
    Inspecting kubernetes cluster
    Inspect kubernetes cluster
    Inspecting juju
    Inspect Juju
    Inspecting kubeflow
    Inspect Kubeflow

    WARNING:  Docker is installed. 
    File "/etc/docker/daemon.json" does not exist. 
    You should create it and add the following lines: 
    {
        "insecure-registries" : ["localhost:32000"] 
    }
    and then restart docker with: sudo systemctl restart docker
    Building the report tarball
    Report tarball is at /var/snap/microk8s/2530/inspection-report-20211019_140011.tar.gz
    ```
We can see now that microk8s is installed, operational, and has deployed the `dns`, `dashboard`, and `storage` services needed for deploying our local instance of Kubeflow.

To continue with the installation of Kubeflow on top of this microk8s deployment, [please move to the README.md contained within the `Kubeflow` directory of this repository](../kubeflow/README.md)