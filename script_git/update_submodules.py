import os
import subprocess

repos = [
    "PCB_VSDSquadron_Pro",
    "PCB_VSDSquadron_Mini",
    "PCB_VSDSquadron_FM",
    "PCB_VSDSquadron_Ultra",
    "PCB_VSDSquadron_SKY130"
]

def update_submodules(repo_path):
    try:
        print(f"\nUpdating submodules in {repo_path} …")

        # 1. Make sure submodules are initialised
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            cwd=repo_path, check=True
        )

        # 2. Now move each submodule to the branch it tracks (e.g. main) and pull latest
        subprocess.run(
            ["git", "submodule", "update", "--remote", "--recursive"],
            cwd=repo_path, check=True
        )

        # 3. OPTIONAL: fast-forward the recorded commit so the super-project
        #            itself reflects the new submodule SHAs (requires commit)
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", "Bump submodules"], cwd=repo_path)
        subprocess.run(["git", "push"], cwd=repo_path)

        print(f"✅ Submodules updated & on their tracking branch for {repo_path}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update submodules in {repo_path}: {e}")

def main():
    # Script lives two levels beneath the repos
    root_dir = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))

    for repo in repos:
        repo_path = os.path.join(root_dir, repo)
        if os.path.isdir(repo_path):
            update_submodules(repo_path)
        else:
            print(f"⚠️  Repository {repo} not found at {repo_path}")

if __name__ == "__main__":
    main()
