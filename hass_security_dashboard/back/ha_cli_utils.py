import subprocess
import json

class HACliUnavailable(Exception):
    """Raised when the `ha` CLI cannot be executed."""
    pass


def run_ha_command(args):
    """Run a Home Assistant CLI command and return stdout.

    Parameters
    ----------
    args: list[str]
        Arguments passed to the `ha` command, e.g. ['core', 'info'].

    Returns
    -------
    str | None
        The command output if successful or ``None`` if the command failed.

    Raises
    ------
    HACliUnavailable
        If the `ha` executable is not found.
    """
    try:
        result = subprocess.run(
            ["ha", *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except FileNotFoundError as exc:
        raise HACliUnavailable("ha CLI not found") from exc
    except subprocess.CalledProcessError as exc:
        print(f"ha {' '.join(args)} failed: {exc}")
        return None


def get_addon_info(slug):
    """Return information about an add-on using the HA CLI.

    The return dict contains ``version`` and ``update_available`` when
    available. ``None`` is returned if the CLI is unavailable or the
    command fails.
    """
    try:
        out = run_ha_command(["addons", "info", slug, "--raw-json"])
        if not out:
            return None
        data = json.loads(out)
        return {
            "version": data.get("version"),
            "update_available": data.get("update_available"),
            "state": data.get("state"),
        }
    except (HACliUnavailable, json.JSONDecodeError) as exc:
        print(f"Add-on info for {slug} failed: {exc}")
        return None


def get_core_info():
    """Return version information for Home Assistant core."""
    try:
        out = run_ha_command(["core", "info", "--raw-json"])
        if not out:
            return None
        data = json.loads(out)
        return {
            "version": data.get("version"),
            "update_available": data.get("version") != data.get("version_latest"),
        }
    except (HACliUnavailable, json.JSONDecodeError) as exc:
        print(f"Core info failed: {exc}")
        return None
