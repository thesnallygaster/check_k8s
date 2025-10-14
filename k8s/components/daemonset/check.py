from k8s.result import Result

from .resource import DaemonSet


def check_daemonsets(items, expressions):
    """Checks the health of the provided DaemonSets

    Documentation:
    https://kubernetes.io/docs/concepts/workloads/controllers/daemonset
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#list-all-namespaces-29

    :param items: List of DaemonSets
    :return: DaemonSets health summary
    """

    return Result(DaemonSet, items, expressions)
