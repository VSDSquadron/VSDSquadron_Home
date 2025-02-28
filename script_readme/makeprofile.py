#!/usr/bin/env python3
import os
import re
import shutil
import subprocess

def copy_readme_and_images(
    source_readme_path,
    destination_repo_path,
    readme_destination_subdir="profile"
):
    """
    Copies the README and all referenced images from source_readme_path
    into destination_repo_path (.github repo). Then pushes changes.
    """
    # 1. Build the absolute path to the .github/profile/ directory
    profile_dir = os.path.join(destination_repo_path, readme_destination_subdir)
    os.makedirs(profile_dir, exist_ok=True)

    # 2. Read the original README
    with open(source_readme_path, 'r', encoding='utf-8') as f:
        readme_contents = f.read()

    # 3. Find all markdown image references: ![alt](relative/path/to/image.jpg)
    pattern = r"!\[.*?\]\((.*?)\)"
    image_paths = re.findall(pattern, readme_contents)

    # 4. Copy the images
    readme_root_dir = os.path.dirname(os.path.abspath(source_readme_path))
    for img_path in image_paths:
        img_path_normalized = os.path.normpath(img_path)
        abs_img_path = os.path.join(readme_root_dir, img_path_normalized)

        if not os.path.exists(abs_img_path):
            print(f"[WARNING] Referenced image '{img_path}' not found at '{abs_img_path}'.")
            continue

        dst_full_path = os.path.join(destination_repo_path, img_path_normalized)
        os.makedirs(os.path.dirname(dst_full_path), exist_ok=True)

        shutil.copy2(abs_img_path, dst_full_path)
        print(f"[INFO] Copied image: {abs_img_path} -> {dst_full_path}")

    # 5. Copy the README into .github/profile/README.md
    dest_readme_path = os.path.join(profile_dir, "README.md")
    with open(dest_readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_contents)

    print(f"\n[SUCCESS] README.md successfully copied to: {dest_readme_path}")

    # 6. Push changes to the .github repo
    #    We'll do a simple add-commit-push via subprocess.
    #    Make sure your system is authenticated with GitHub (SSH key or credential manager).
    try:
        print("[INFO] Staging changes in .github repository...")
        subprocess.run(["git", "add", "."], cwd=destination_repo_path, check=True)
        
        print("[INFO] Committing changes in .github repository...")
        commit_message = "Automated update of organization profile README and images"
        subprocess.run(["git", "commit", "-m", commit_message], cwd=destination_repo_path, check=True)

        print("[INFO] Pushing changes to remote...")
        subprocess.run(["git", "push"], cwd=destination_repo_path, check=True)

        print("[SUCCESS] Changes pushed to the .github repository.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git command failed with exit code {e.returncode}. "
               "Check credentials, remote branches, or local untracked files.")


if __name__ == "__main__":
    """
    Example usage:
      python copy_readme_images_and_push.py

    Make sure:
      - This script is located in VSDSquadron/script_readme/.
      - The main README.md is at ../README.md relative to this script.
      - The .github repo is a sibling of VSDSquadron, or adjust the paths accordingly.
      - The .github repo is already initialized with 'git init' and has a valid remote.
      - Your environment is set up to push (SSH keys or personal access token).
    """
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    SOURCE_README = os.path.join(SCRIPT_DIR, "..", "README.md")  # VSDSquadron/README.md
    DESTINATION_REPO = os.path.join(SCRIPT_DIR, "..", "..", ".github")  # sibling to VSDSquadron

    copy_readme_and_images(SOURCE_README, DESTINATION_REPO)
