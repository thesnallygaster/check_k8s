from .pod import check_pods
from .daemonset import check_daemonsets
from .deployment import check_deployments
from .node import check_nodes
from .persistentvolumeclaim import check_persistentvolumeclaims
from .statefulset import check_statefulsets


# Purpose
# -------
# 1) Provide enum for Argparse "Resource choices"
# 2) Resolve how to obtain and process health data

MAPPINGS = dict(
    # resource_name, (check_func, is_core)
    pods=(check_pods, True),
    nodes=(check_nodes, True),
    daemonsets=(check_daemonsets, False),
    deployments=(check_deployments, False),
    persistentvolumeclaims=(check_persistentvolumeclaims, True),
    statefulsets=(check_statefulsets, False),
)
