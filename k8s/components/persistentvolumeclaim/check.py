from k8s.result import Result

from .resource import PersistentVolumeClaim


def check_persistentvolumeclaims(items, expressions):
    """Checks the health of the provided PersistentVolumeClaims

    Documentation:
    https://kubernetes.io/docs/concepts/workloads/controllers/persistentvolumeclaim
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#list-all-namespaces-29

    :param items: List of PersistentVolumeClaims
    :return: PersistentVolumeClaims health summary
    """

    return Result(PersistentVolumeClaim, items, expressions)
