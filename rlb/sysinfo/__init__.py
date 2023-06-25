"""Provides system information for system under test."""

from platform import uname
import json
import subprocess


class SystemInfo:
    """Provides system information for system under test."""

    def __init__(self):
        """Initialize SystemInfo class."""
        self._system = uname()

        # Get system profile data if we're on MacOS
        if self.os() == "MacOS":
            spd = subprocess.Popen(
                [
                    "system_profiler",
                    "-json",
                    "SPDisplaysDataType",
                    "SPHardwareDataType",
                ],
                stdout=subprocess.PIPE,
            )
            data = json.loads(spd.communicate()[0].decode("utf-8"))

            self._cpu = data["SPHardwareDataType"][0]["chip_type"]
            self._cpu_cores = data["SPHardwareDataType"][0]["number_processors"].split(
                " "
            )[1]
            self._gpu = data["SPDisplaysDataType"][0]["sppci_model"]
            self._gpu_cores = data["SPDisplaysDataType"][0]["sppci_cores"]
            self._ram = data["SPHardwareDataType"][0]["physical_memory"]

    def os(self):
        """Return operating system name."""
        if self._system.system == "Linux":
            return "Linux"
        elif self._system.system == "Darwin":
            return "MacOS"
        elif self._system.system == "Windows":
            return "Windows"
        else:
            return self._system.system

    def arch(self):
        """Return system architecture."""
        return self._system.machine

    def gpu(self):
        """Return GPU info."""
        if self.os() == "MacOS":
            return f"{self._gpu} - {self._gpu_cores} cores"
        else:
            return "Unknown"

    def cpu(self):
        """Return CPU info."""
        if self.os() == "MacOS":
            cores = self._cpu_cores.split(":")[0]
            pcores = self._cpu_cores.split(":")[1]
            ecores = self._cpu_cores.split(":")[2]

            return (
                f"{self._cpu} - "
                f"{cores} cores ({pcores} performance and {ecores} efficiency)"
            )
        else:
            return "Unknown"


def basic(format="text"):
    """Return basic system info.

    Args:
      format(str): Format to return data in. Supported formats are "text" and "json".

    Returns:
      str: System info in the requested format.
    """
    sysinfo = SystemInfo()

    if format == "text":
        return f"""OS: {sysinfo.os()}
ARCH: {sysinfo.arch()}
CPU: {sysinfo.cpu()}
GPU: {sysinfo.gpu()}
RAM: {sysinfo._ram}
"""
    elif format == "json":
        return json.dumps(
            {
                "os": sysinfo.os(),
                "arch": sysinfo.arch(),
                "cpu": sysinfo.cpu(),
                "gpu": sysinfo.gpu(),
                "ram": sysinfo._ram,
            }
        )
    else:
        return "Format Not Supported"


def threads():
    """Return suggested number of cpu threads to use."""
    sysinfo = SystemInfo()
    if sysinfo.os() == "MacOS":
        return int(sysinfo._cpu_cores.split(":")[1])
    else:
        return 4
