""""Argo Workflow for building Jupyter Web App's OCI image using Kaniko"""
from kubeflow.kubeflow.cd import config, kaniko_builder


def create_workflow(name=None, namespace=None, bucket=None, **kwargs):
    """
    Args:
        name: Name to give to the workflow. This can also be used to name
              things associated with the workflow.
    """
    builder = kaniko_builder.Builder(name=name, namespace=namespace, bucket=bucket, **kwargs)

    return builder.build(dockerfile="components/crud-web-apps/jupyter/Dockerfile",
                         context="components/crud-web-apps/",
                         destination=config.JUPYTER_WEB_APP_IMAGE)
