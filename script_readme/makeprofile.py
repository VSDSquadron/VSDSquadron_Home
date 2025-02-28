#!/usr/bin/env python3
import os
import re
import shutil
import subprocess

def copy_readme_and_images_into_profile(
    source_readme_path,
    destination_repo_path,
    readme_destination_subdir="profile"
):
    """
    Copies the README and all referenced images from source_readme_path
    into the .github/profile/ folder, then stages, commits, and pushes
    those changes.
    """
    # 1. Construct the absolute path to .github/profile/
    profile_dir = os.path.join(destination_repo_path, readme_destination_subdir)
    os.makedirs(profile_dir, exist_ok=True)

    # 2. Read the original README
    with open(source_readme_path, 'r', encoding='utf-8') as f:
        readme_contents = f.read()

    # 3. Find all local images referenced with the pattern:
    #    ![some alt text](path/to/image.jpg)
    pattern = r"!\[.*?\]\((.*?)\)"
    image_paths = re.findall(pattern, readme_contents)

    # 4. Copy each image into .github/profile/<same-subfolder-structure>
    readme_root_dir = os.path.dirname(os.path.abspath(source_readme_path))
    for img_path in image_paths:
        img_path_normalized = os.path.normpath(img_path)  # e.g. "VSDSquadron_SKY130/squadron_sky130_TOP.jpg"
        abs_img_path = os.path.join(readme_root_dir, img_path_normalized)

        if not os.path.exists(abs_img_path):
            print(f"[WARNING] Referenced image '{img_path}' not found at '{abs_img_path}'.")
            continue

        # Store images within .github/profile/, not just .github/
        dst_full_path = os.path.join(profile_dir, img_path_normalized)
        os.makedirs(os.path.dirname(dst_full_path), exist_ok=True)

        shutil.copy2(abs_img_path, dst_full_path)
        print(f"[INFO] Copied image: {abs_img_path} -> {dst_full_path}")

    # 5. Copy the README into .github/profile/README.md
    dest_readme_path = os.path.join(profile_dir, "README.md")
    with open(dest_readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_contents)

    print(f"\n[SUCCESS] README.md copied to: {dest_readme_path}")

    # 6. Add/Commit/Push changes from .github repository
    #    Make sure your environment is authenticated to push.
    try:
        print("[INFO] Staging changes in .github repository...")
        subprocess.run(["git", "add", "."], cwd=destination_repo_path, check=True)
        
        print("[INFO] Committing changes in .github repository...")
        commit_message = "Automated update of .github/profile README and images"
        subprocess.run(["git", "commit", "-m", commit_message], cwd=destination_repo_path, check=True)

        print("[INFO] Pushing changes to remote...")
        subprocess.run(["git", "push"], cwd=destination_repo_path, check=True)

        print("[SUCCESS] Changes pushed to the .github repository.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git command failed with exit code {e.returncode}. "
              "Check your Git credentials, remote config, or untracked files.")

if __name__ == "__main__":
    """
    Example usage:
      python copy_readme_images_profile.py

    Assumptions:
      - This script lives in VSDSquadron/script_readme/
      - Your main VSDSquadron README is at ../README.md
      - Your .github repo is two dirs above, e.g. ../.., 
        and is a valid git repo with a configured remote.
    """
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Adjust paths as needed
    SOURCE_README = os.path.join(SCRIPT_DIR, "..", "README.md")      # e.g. VSDSquadron/README.md
    DESTINATION_REPO = os.path.join(SCRIPT_DIR, "..", "..", ".github")

    copy_readme_and_images_into_profile(SOURCE_README, DESTINATION_REPO)
