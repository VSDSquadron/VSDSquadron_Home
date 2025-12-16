import os
import subprocess
from typing import List

repos = [
    "PCB_VSDSquadron_Pro",
    "PCB_VSDSquadron_Mini",
    "PCB_VSDSquadron_FM",
    "PCB_VSDSquadron_Ultra",
    "PCB_VSDSquadron_SKY130",
]


def run_git(command: List[str], cwd: str, check: bool = True, capture_output: bool = False):
    """Helper to execute git commands with consistent settings."""
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=capture_output,
        text=True if capture_output else None,
    )


def list_submodules(repo_path: str) -> List[str]:
    """
    Reads .gitmodules to determine all submodule paths.
    Returns an empty list if the repo has no submodules.
    """
    gitmodules = os.path.join(repo_path, ".gitmodules")
    if not os.path.isfile(gitmodules):
        return []

    try:
        result = run_git(
            ["git", "config", "--file", ".gitmodules", "--get-regexp", "path"],
            cwd=repo_path,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        return []

    paths = []
    for line in result.stdout.strip().splitlines():
        try:
            _, path = line.split(" ", 1)
        except ValueError:
            continue
        paths.append(path.strip())
    return paths


def pull_all_submodules(repo_path: str):
    """Recursively runs `git pull` inside every submodule under repo_path."""
    submodules = list_submodules(repo_path)
    if not submodules:
        return

    for rel_path in submodules:
        submodule_dir = os.path.join(repo_path, rel_path)
        if not os.path.isdir(submodule_dir):
            print(f"Skipping missing submodule {rel_path} in {repo_path}")
            continue

        print(f"Running git pull in {submodule_dir}")
        try:
            run_git(["git", "pull"], cwd=submodule_dir)
        except subprocess.CalledProcessError as err:
            print(f"Failed to pull {rel_path}: {err}")
            continue

        pull_all_submodules(submodule_dir)


def update_submodules(repo_path: str):
    try:
        print(f"\nUpdating submodules in {repo_path}")

        # Ensure the submodule working trees exist before pulling.
        run_git(["git", "submodule", "update", "--init", "--recursive"], cwd=repo_path)

        pull_all_submodules(repo_path)

        run_git(["git", "add", "."], cwd=repo_path)
        commit = run_git(
            ["git", "commit", "-m", "Update submodules"],
            cwd=repo_path,
            check=False,
        )

        if commit.returncode == 0:
            run_git(["git", "push"], cwd=repo_path)
            print(f"Submodule updates committed and pushed for {repo_path}")
        else:
            print(f"No submodule changes to commit for {repo_path}")

    except subprocess.CalledProcessError as exc:
        print(f"Failed to update submodules in {repo_path}: {exc}")


def main():
    # Script lives two levels beneath the repos
    root_dir = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))

    for repo in repos:
        repo_path = os.path.join(root_dir, repo)
        if os.path.isdir(repo_path):
            update_submodules(repo_path)
        else:
            print(f"Repository {repo} not found at {repo_path}")


if __name__ == "__main__":
    main()
