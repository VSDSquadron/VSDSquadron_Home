import os
import subprocess

# List of repositories
repos = [
    "PCB_VSDSquadron_Pro",
    "PCB_VSDSquadron_Mini",
    "PCB_VSDSquadron_FM",
    "PCB_VSDSquadron_Ultra",
    "PCB_VSDSquadron_SKY130"
]

def update_submodules(repo_path):
    try:
        print(f"\nUpdating submodules in {repo_path}...")
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], cwd=repo_path, check=True)
        print(f"✅ Submodules updated for {repo_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update submodules in {repo_path}: {e}")

def main():
    # Assuming this script is in the same root where repos are cloned
    root_dir = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))

    for repo in repos:
        repo_path = os.path.join(root_dir, repo)
        if os.path.isdir(repo_path):
            update_submodules(repo_path)
        else:
            print(f"⚠️  Repository {repo} not found at {repo_path}")

if __name__ == "__main__":
    main()
