# Kubeflow Installation

There are many [distributions with packaging](https://www.kubeflow.org/docs/distributions/) that exist for deploying Kubeflow into different environment, but here we're going to utilize kustomize and deploy our local installation of Kubeflow using the [project provided manifests](https://github.com/kubeflow/manifests).

We've already downloaded the manifests and made a few local edits required for running Kubeflow on top of microk8s running Kubernetes versions > 1.19. Please follow the instructions below for ensuring a stable environment post installation.

1. Change directories into the `manifests` directory
   ```bash
   $ cd manifests
   ```

2. We will utilize the single command install using the command below
   ```bash
   $ while ! .././kustomize build example | microk8s.kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done
   ```

```text
**NOTE** THAT INSTALLATION CAN TAKE UPWARDS OF 10 MINUTES DEPENDING ON THE RESOURCES AVAILABLE ON YOUR WORKSTATION
```

Verify the status of the Kubeflow pods by using the `microk8s.kubectl get pods -A -w` command. The `-w` flag will watch the status of the output of the `get pods -A` command.

 Your output should look similar to what is shown below. `SEE THE NOTE ABOVE`.
