package controllers

import (
	"reflect"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func TestUpdateNamespaceLabels(t *testing.T) {
	name := "test-namespace"
	tests := []map[string]*corev1.Namespace{
		map[string]*corev1.Namespace{
			"current": &corev1.Namespace{
				ObjectMeta: metav1.ObjectMeta{
					Name: name,
				},
			},
			"expected": &corev1.Namespace{
				ObjectMeta: metav1.ObjectMeta{
					Labels: map[string]string{
						"katib-metricscollector-injection":      "enabled",
						"serving.kubeflow.org/inferenceservice": "enabled",
						"pipelines.kubeflow.org/enabled":        "true",
						"app.kubernetes.io/part-of":             "kubeflow-profile",
					},
					Name: name,
				},
			},
		},
		map[string]*corev1.Namespace{
			"current": &corev1.Namespace{
				ObjectMeta: metav1.ObjectMeta{
					Labels: map[string]string{
						"user-name":                             "Jim",
						"serving.kubeflow.org/inferenceservice": "disabled",
					},
					Name: name,
				},
			},
			"expected": &corev1.Namespace{
				ObjectMeta: metav1.ObjectMeta{
					Labels: map[string]string{
						"user-name":                             "Jim",
						"katib-metricscollector-injection":      "enabled",
						"serving.kubeflow.org/inferenceservice": "disabled",
						"pipelines.kubeflow.org/enabled":        "true",
						"app.kubernetes.io/part-of":             "kubeflow-profile",
					},
					Name: name,
				},
			},
		},
	}
	for _, test := range tests {
		updateNamespaceLabels(test["current"])
		if !reflect.DeepEqual(test["expected"], test["current"]) {
			t.Errorf("Expect:\n%v; Output:\n%v", test["current"], test["expected"])
		}
	}
}
