from collections import namedtuple
from enum import Enum

from k8s.consts import NaemonState

from ..resource import Resource, NaemonStatus


StatefulSets = namedtuple("StatefulSets", ["current", "desired", "available", "ready", "updated"])


class StatefulSet(Resource):
    class PerfMap(Enum):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        DEGRADED = "degraded"

    def __init__(self, data, *args, **kwargs):
        super(StatefulSet, self).__init__(data, *args, **kwargs)

        if self._status.get("availableReplicas") == self._data.get("spec").get("replicas"):
            self._status["conditions"] = [
                {
                    "type": "Available",
                    "status": "True",
                    "reason": "availableReplicas",
                    "message": "StatefulSet has desired availability."
                }
            ]
        else:
            self._status["conditions"] = [
                {
                    "type": "Available",
                    "status": "False",
                    "reason": "availableReplicas",
                    "message": "StatefulSet does not have desired availability."
                }
            ]

        self.statefulsets = StatefulSets(
            self._status.get("currentReplicas", 0),
            self._data.get("spec", 0).get("replicas", 0),
            self._status.get("availableReplicas", 0),
            self._status.get("readyReplicas", 0),
            self._status.get("updatedReplicas", 0),
        )

    def _get_status(self, cnd_type, cnd_status):
        dsets = self.statefulsets

        if cnd_type == "Available":
            if cnd_status == "True":
                return NaemonStatus(NaemonState.OK, self.perf.AVAILABLE)
            else:
                return NaemonStatus(NaemonState.CRITICAL, self.perf.UNAVAILABLE)
        elif dsets.available < dsets.desired or dsets.current < dsets.desired:
            if dsets.available != 0 and dsets.current != 0:
                return NaemonStatus(NaemonState.WARNING, self.perf.DEGRADED)
            return NaemonStatus(NaemonState.CRITICAL, self.perf.UNAVAILABLE)
