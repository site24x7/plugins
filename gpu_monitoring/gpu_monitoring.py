#!/usr/bin/env python3

from __future__ import annotations
import json
import subprocess
import argparse
from typing import Any

PLUGIN_VERSION = 1
HEARTBEAT = True

# Note: cuda_version is NOT in query-gpu fields, we get it separately.
SMM_FIELDS = [
    "index",
    "name",
    "temperature.gpu",
    "utilization.gpu",
    "memory.total",
    "memory.used",
    "power.draw",
    "enforced.power.limit",
    "fan.speed",
    "driver_version"
]


def run_nvidia_smi(nvidia_smi_path: str, fields: list[str]) -> str:
    query = ",".join(fields)
    cmd = [
        nvidia_smi_path,
        "--query-gpu=" + query,
        "--format=csv,noheader,nounits",
    ]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return out.decode("utf-8", errors="replace").strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            "nvidia-smi returned non-zero: "
            + e.output.decode("utf-8", errors="replace")
        ) from e
    except FileNotFoundError:
        raise RuntimeError(
            "nvidia-smi not found at '{}' (is NVIDIA driver installed?)".format(
                nvidia_smi_path
            )
        )


def get_cuda_version(nvidia_smi_path: str) -> str | None:
    """
    Call plain `nvidia-smi` and parse the 'CUDA Version: X.Y' from the header line,
    which is how many tools get CUDA version when it's not a query-gpu field. [web:84][web:85][web:88]
    """
    try:
        out = subprocess.check_output(
            [nvidia_smi_path], stderr=subprocess.STDOUT
        ).decode("utf-8", errors="replace")
    except Exception:
        return None

    for line in out.splitlines():
        if "CUDA Version" in line:
            # Example: "NVIDIA-SMI 560.35.03    Driver Version: 560.35.03    CUDA Version: 12.5"
            parts = line.split("CUDA Version")
            if len(parts) < 2:
                continue
            # Take the text after "CUDA Version"
            right = parts[1]
            # Strip ": " and other separators
            right = right.replace(":", " ").strip()
            # First token should be version like "12.5"
            ver = right.split()[0] if right.split() else ""
            return ver or None
    return None


def parse_csv_lines(output: str, fields: list[str]) -> list[dict[str, str]]:
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    gpus: list[dict[str, str]] = []
    for ln in lines:
        cols = [c.strip() for c in ln.split(",")]
        if len(cols) < len(fields):
            mapped: dict[str, str] = {}
            rev_fields = list(reversed(fields))
            rev_cols = list(reversed(cols))
            j = 0
            for f in rev_fields:
                if j < len(rev_cols):
                    mapped[f] = rev_cols[j]
                else:
                    mapped[f] = ""
                j += 1
            row: list[str] = []
            for f in fields:
                row.append(mapped.get(f, ""))
            cols = row
        gpu: dict[str, str] = {}
        for f, v in zip(fields, cols):
            gpu[f] = v
        gpus.append(gpu)
    return gpus


def safe_float(s: str) -> float | None:
    try:
        s2 = s.strip()
        if s2 == "":
            return None
        return float(s2)
    except Exception:
        return None


def build_flat_output(
    parsed_gpus: list[dict[str, str]], cuda_version: str | None
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": "true",
    }
    units: dict[str, str] = {}

    if not parsed_gpus:
        result["Average Memory - Percentage"] = 0.0
        result["status"] = 0
        result["units"] = units
        if cuda_version:
            result["CUDA Version"] = "v {}".format(cuda_version)
        return result

    first = parsed_gpus[0]

    driver_version = first.get("driver_version", "").strip()
    if driver_version:
        result["Driver Version"] = "v {}".format(driver_version)

    if cuda_version:
        result["CUDA Version"] = "v {}".format(cuda_version)

    mem_pcts: list[float] = []

    for g in parsed_gpus:
        idx_raw = g.get("index", "").strip()
        if idx_raw == "":
            idx_raw = "0"
        try:
            idx = int(idx_raw)
        except ValueError:
            idx = 0

        gpu_key_prefix = "GPU{}".format(idx)

        name = g.get("name", "").strip()
        if name:
            result[gpu_key_prefix] = name

        mem_total = safe_float(g.get("memory.total", ""))
        mem_used = safe_float(g.get("memory.used", ""))

        if mem_used is not None:
            result["{} - Memory".format(gpu_key_prefix)] = mem_used
            units["{} - Memory".format(gpu_key_prefix)] = "MB"

        if mem_total is not None:
            result["{} Total Memory".format(gpu_key_prefix)] = "{} MB".format(
                int(mem_total)
            )

        if mem_total is not None and mem_total > 0 and mem_used is not None:
            mem_pct = (mem_used / mem_total) * 100.0
            mem_pcts.append(mem_pct)

        util = safe_float(g.get("utilization.gpu", ""))
        if util is not None:
            result["{} - Utilization".format(gpu_key_prefix)] = util
            units["{} - Utilization".format(gpu_key_prefix)] = "%"

        temp = safe_float(g.get("temperature.gpu", ""))
        if temp is not None:
            result["{} - Temperature".format(gpu_key_prefix)] = temp
            units["{} - Temperature".format(gpu_key_prefix)] = "C"

        power_draw = safe_float(g.get("power.draw", ""))
        if power_draw is not None:
            result["{} - Power Draw".format(gpu_key_prefix)] = power_draw
            units["{} - Power Draw".format(gpu_key_prefix)] = "W"

        power_limit = safe_float(g.get("enforced.power.limit", ""))
        if power_limit is not None:
            result["{} - Power Limit".format(gpu_key_prefix)] = "{} W".format(
                int(power_limit)
            )

        fan_speed = safe_float(g.get("fan.speed", ""))
        if fan_speed is not None:
            result["{} - Fan Speed".format(gpu_key_prefix)] = fan_speed
            units["{} - Fan Speed".format(gpu_key_prefix)] = "%"

    if mem_pcts:
        avg_mem_pct = sum(mem_pcts) / len(mem_pcts)
        result["Average Memory - Percentage"] = round(avg_mem_pct, 2)
        units["Average Memory - Percentage"] = "%"

    result["units"] = units
    return result


def metricCollector(params: dict | None = None) -> dict[str, Any]:
    """
    Entry point expected by Site24x7 Python plugins:
    must RETURN a dict with metrics, not None.
    """
    nvidia_smi_path = "nvidia-smi"
    fields = ",".join(SMM_FIELDS)

    try:
        raw = run_nvidia_smi(nvidia_smi_path, fields.split(","))
        parsed = parse_csv_lines(raw, fields.split(","))
        cuda_ver = get_cuda_version(nvidia_smi_path)
        result = build_flat_output(parsed, cuda_ver)
    except Exception as e:
        result = {
            "heartbeat_required": "true",
            "msg": str(e),
            "plugin_version": PLUGIN_VERSION,
            "status": 0,
            "units": {},
        }

    return result


def run(param=None) -> dict[str, Any]:
    return metricCollector(param)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="GPU metrics via nvidia-smi with flattened JSON output."
    )
    parser.add_argument(
        "--nvidia-smi-path",
        default="nvidia-smi",
        help="Path to nvidia-smi binary (default: nvidia-smi)",
    )
    parser.add_argument(
        "--fields",
        default=",".join(SMM_FIELDS),
        help="Comma-separated query fields for nvidia-smi",
    )
    parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print JSON"
    )
    args = parser.parse_args()

    try:
        raw = run_nvidia_smi(args.nvidia_smi_path, args.fields.split(","))
        parsed = parse_csv_lines(raw, args.fields.split(","))
        cuda_ver = get_cuda_version(args.nvidia_smi_path)
        out = build_flat_output(parsed, cuda_ver)
    except Exception as e:
        out = {
            "heartbeat_required": "true",
            "msg": str(e),
            "plugin_version": PLUGIN_VERSION,
            "status": 0,
            "units": {},
        }

    if args.pretty:
        print(json.dumps(out, indent=4))
    else:
        print(json.dumps(out))
