from collections import namedtuple
from enum import Enum

from k8s.consts import NaemonState

from ..resource import Resource, NaemonStatus


PersistentVolumeClaims = namedtuple("PersistentVolumeClaims", ["phase", "capacity", "accessmodes"])


class PersistentVolumeClaim(Resource):
    class PerfMap(Enum):
        AVAILABLE = "available"
        BOUND = "bound"
        RELEASED = "released"
        FAILED = "failed"

    def __init__(self, data, *args, **kwargs):
        super(PersistentVolumeClaim, self).__init__(data, *args, **kwargs)

        if self._status.get("phase") == "Bound":
            self._status["conditions"] = [
                {
                    "type": "Bound",
                    "status": "True",
                    "reason": "phase",
                    "message": "PersistentVolume is bound to a claim."
                }
            ]
        elif self._status.get("phase") == "Available":
            self._status["conditions"] = [
                {
                    "type": "Available",
                    "status": "True",
                    "reason": "phase",
                    "message": "PersistentVolume is not yet bound to a claim."
                }
            ]
        elif self._status.get("phase") == "Released":
            self._status["conditions"] = [
                {
                    "type": "Released",
                    "status": "True",
                    "reason": "phase",
                    "message": "PersistentVolumeClam has been deleted but not yet reclaimed by cluster."
                }
            ]
        else:
            self._status["conditions"] = [
                {
                    "type": "Failed",
                    "status": "True",
                    "reason": "phase",
                    "message": "PersistentVolume has failed."
                }
            ]

        self.persistentvolumeclaims = PersistentVolumeClaims(
            self._status.get("phase", 0),
            self._status.get("capacity", 0),
            self._status.get("accessModes", 0),
        )

    def _get_status(self, cnd_type, cnd_status):
        dsets = self.persistentvolumeclaims

        if cnd_type == "Bound" or cnd_type == "Available" or cnd_type == "Relased":
            if cnd_status == "True":
                if cnd_type == "Bound":
                    return NaemonStatus(NaemonState.OK, self.perf.BOUND)
                elif cnd_type == "Available":
                    return NaemonStatus(NaemonState.OK, self.perf.AVAILABLE)
                elif cnd_type == "Released":
                    return NaemonStatus(NaemonState.OK, self.perf.AVAILABLE)
            else:
                return NaemonStatus(NaemonState.CRITICAL, self.perf.FAILED)
        else:
                return NaemonStatus(NaemonState.CRITICAL, self.perf.FAILED)
