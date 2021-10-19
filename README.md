# Zero to Inference with Kubeflow

## Getting Started

This repository houses all of the tools, utilities, and example pipeline implementations for exploring using Kubeflow within their data science / machine learning projects.

Please follow the README's that are provided for each of the [Components](#components) below.

### Installation Flow

The graph below provides the high level overview of the process that should be followed.

[Install Microk8s](./microk8s/README.md) --> [Deploy Kubeflow](./kubeflow/README.md) --> [Deploy Pipeline](./pipeline/README.md) --> [Create Notebook Server](./notebooks/README.md) --> [Upload Notebook and Data](./notebooks/README.md#upload-our-notebook-and-data) --> [Evaluate Served Model](./notebooks/README.md#evaluate-trained-model)

## Components

### Microk8s

The [microk8s directory contains a README](./microk8s/README.md) of all of the necessary commands that will need to be issued to install microk8s on your local development enivornment

### Kubeflow

The [kubeflow directory contains a README](./kubeflow/README.md) of all of the necessary commands that will need to be issued to install Kubeflow on your local microk8s installation.

```text
NOTE: I've made some edits to the default manifests that are provided with Kubeflow to accomodate some of the intricacies of a local deployment of the stack. Please be aware that these manifests are not what are provided on the main repo v1.3 branch.
```

### Kubeflow Pipeline

[Contained in the pipeline directory](./pipeline/src) is a simple [Kubeflow Pipeline](https://www.kubeflow.org/docs/components/pipelines/overview/pipelines-overview/) that will train an MNIST classifier and deploy the trained model using [KFServing](https://www.kubeflow.org/docs/components/kfserving/kfserving/) local to the Kubeflow installation.

### Notebook

[Contained in the notebooks directory is a notebook](./notebooks/MNIST%20Sample%20Test.ipynb) we can use for verifying the deployment of our model. This is done because of the complexity of exposing services external to microk8s (kubernetes) that is outside of the scope of this tutorial.

### Data

[Contained in the data directory](./data) are some images we can classify that will allow us to test the functionality of the model we've deployed.

These images will need to be uploaded to the notebook server once it has been deployed.

## Directory Structure

This directory structure tries to mirror the structure used within the [Cookiecutter Data Science](https://github.com/drivendata/cookiecutter-data-science) project. 