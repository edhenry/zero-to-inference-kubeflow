from typing import Dict

import kfp.compiler as compiler
import kfp.components as components
import kfp.dsl as dsl
from kfp import components

NAMESPACE = "kubeflow-user-example-com"

@dsl.pipeline(
name='Zero to Inference with Kubeflow',
description='Example pipeline for the Dell Data Science Week 2021 Zero to Inference with Kubeflow Session'
)
def pipeline(model_export_dir: str ='/mnt',
             train_steps: str ='200',
             learning_rate: str ='0.01',
             batch_size: str ='100',
             pvc_name: str ='ztik-pvc') -> None:
    """
    Simple pipeline definition for defining and deploying a Kubeflow Pipeline

    Args:
        model_export_dir (str, optional): Directory where we want to save our model. Defaults to './'.
        train_steps (str, optional): Number of training steps to take. Defaults to '200'.
        learning_rate (str, optional): Learning rate to use for our model. Defaults to '0.01'.
        batch_size (str, optional): Batch size for mini-batching. Defaults to '100'.
        pvc_name (str, optional): Name of the local k8s PVC used within the pipeline. Defaults to 'ztik'.
    """
    vop: dsl.VolumeOp = dsl.VolumeOp(
    name="ztik-pvc",
    resource_name=pvc_name,
    size="1Gi",
    modes=dsl.VOLUME_MODE_RWM
    ).set_display_name("Create Pipeline PVC")

    # Dict to hold all of the operators so we can reuse them across conditional 
    # executions of certain portions of the graph
    ops: Dict[str, dsl.ContainerOp] = {}

    ops['train'] = dsl.ContainerOp(name="Train MNIST Classifier",
                            image="edhenry/ztik-model",
                            arguments=[
                                "/opt/model.py",
                                "--tf-export-dir", model_export_dir,
                                "--tf-train-steps", train_steps,
                                "--tf-batch-size", batch_size,
                                "--tf-learning-rate", learning_rate
                            ],
                            pvolumes={'/mnt': vop.volume}).set_display_name("Train MNIST Classifier")
    
    ops['train'].after(vop)

    serveOp = components.load_component_from_url("https://raw.githubusercontent.com/kubeflow/pipelines/master/components/kubeflow/kfserving/component.yaml")

    ops['serve'] = serveOp(action="apply", 
                           namespace="kubeflow-user-example-com",
                           model_name="mnist-sample-1", 
                           model_uri=f"pvc://{vop.outputs['name']}",
                           framework="tensorflow",
                           enable_istio_sidecar=False)

    ops['serve'].after(ops['train'])
    
if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(pipeline, "ztik.yaml")
