from k8s.result import Result

from .resource import StatefulSet


def check_statefulsets(items, expressions):
    """Checks the health of the provided StatefulSets

    Documentation:
    https://kubernetes.io/docs/concepts/workloads/controllers/statefulset
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#list-all-namespaces-29

    :param items: List of StatefulSets
    :return: StatefulSets health summary
    """

    return Result(StatefulSet, items, expressions)
