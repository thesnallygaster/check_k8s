from collections import namedtuple
from enum import Enum

from k8s.consts import NaemonState

from ..resource import Resource, NaemonStatus


DaemonSets = namedtuple("DaemonSets", ["current", "desired", "available", "misscheduled", "ready", "unavailable"])


class DaemonSet(Resource):
    class PerfMap(Enum):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        DEGRADED = "degraded"
        UNSCHEDULABLE = "unschedulable"

    def __init__(self, data, *args, **kwargs):
        super(DaemonSet, self).__init__(data, *args, **kwargs)

        if self._status.get("numberAvailable") == self._status.get("desiredNumberScheduled"):
            self._status["conditions"] = [
                {
                    "type": "Available",
                    "status": "True",
                    "reason": "numberAvailable",
                    "message": "DaemonSet has desired availability."
                }
            ]
        elif self._status.get("desiredNumberScheduled") == 0:
            self._status["conditions"] = [
                {
                    "type": "Unschedulable",
                    "status": "True",
                    "reason": "desiredNumberScheduled",
                    "message": "DaemonSet cannot be scheduled."
                }
            ]
        else:
            self._status["conditions"] = [
                {
                    "type": "Available",
                    "status": "False",
                    "reason": "currentNumberScheduled",
                    "message": "DaemonSet does not have desired availability."
                }
            ]

        self.daemonsets = DaemonSets(
            self._status.get("currentNumberScheduled", 0),
            self._status.get("desiredNumberScheduled", 0),
            self._status.get("numberAvailable", 0),
            self._status.get("numberMisscheduled", 0),
            self._status.get("numberReady", 0),
            self._status.get("numberUnavailable", 0),
        )

    def _get_status(self, cnd_type, cnd_status):
        dsets = self.daemonsets

        if dsets.desired == 0:
            return NaemonStatus(NaemonState.OK, self.perf.UNSCHEDULABLE)
        elif cnd_type == "Available":
            if cnd_status == "True":
                return NaemonStatus(NaemonState.OK, self.perf.AVAILABLE)
            else:
                return NaemonStatus(NaemonState.CRITICAL, self.perf.UNAVAILABLE)
        elif dsets.available < dsets.desired or dsets.current < dsets.desired:
            if dsets.available != 0 and dsets.current != 0:
                return NaemonStatus(NaemonState.WARNING, self.perf.DEGRADED)
            return NaemonStatus(NaemonState.CRITICAL, self.perf.UNAVAILABLE)
