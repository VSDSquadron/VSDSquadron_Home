import argparse
import os
import re
import shutil
import subprocess


def clear_files(target_folder):
    """Deletes existing .jpg and .pdf files from the target folder."""
    for entry in os.listdir(target_folder):
        entry_path = os.path.join(target_folder, entry)
        if not os.path.isfile(entry_path):
            continue

        if entry.lower().endswith((".jpg", ".pdf")):
            os.remove(entry_path)


def copy_files(source_folder, target_folder):
    """Copies .jpg, .pdf, and bom.csv files from source to target folder."""
    for ext in [".jpg", ".pdf", "bom.csv"]:
        if os.path.exists(source_folder):
            shutil.copytree(
                source_folder,
                target_folder,
                dirs_exist_ok=True,
                ignore=lambda _, files: [f for f in files if not f.endswith(ext)],
            )


def copy_readme_and_images_into_profile(
    source_readme_path,
    destination_repo_path,
    readme_destination_subdir="profile",
    push_changes=True,
):
    """
    Copies the README and all referenced images from source_readme_path
    into the .github/profile/ folder, then optionally stages, commits,
    and pushes those changes.
    """
    profile_dir = os.path.join(destination_repo_path, readme_destination_subdir)
    os.makedirs(profile_dir, exist_ok=True)

    with open(source_readme_path, "r", encoding="utf-8") as f:
        readme_contents = f.read()

    pattern = r"!\[.*?\]\((.*?)\)"
    image_paths = re.findall(pattern, readme_contents)

    readme_root_dir = os.path.dirname(os.path.abspath(source_readme_path))
    for img_path in image_paths:
        img_path_normalized = os.path.normpath(img_path)
        abs_img_path = os.path.join(readme_root_dir, img_path_normalized)

        if not os.path.exists(abs_img_path):
            print(f"[WARNING] Referenced image '{img_path}' not found at '{abs_img_path}'.")
            continue

        dst_full_path = os.path.join(profile_dir, img_path_normalized)
        os.makedirs(os.path.dirname(dst_full_path), exist_ok=True)

        shutil.copy2(abs_img_path, dst_full_path)
        print(f"[INFO] Copied image: {abs_img_path} -> {dst_full_path}")

    dest_readme_path = os.path.join(profile_dir, "README.md")
    with open(dest_readme_path, "w", encoding="utf-8") as f:
        f.write(readme_contents)

    print(f"\n[SUCCESS] README.md copied to: {dest_readme_path}")

    if not push_changes:
        return

    try:
        print("[INFO] Staging changes in .github repository...")
        subprocess.run(["git", "add", "."], cwd=destination_repo_path, check=True)

        print("[INFO] Committing changes in .github repository...")
        commit_message = "Automated update of .github/profile README and images"
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=destination_repo_path,
            check=True,
        )

        print("[INFO] Pushing changes to remote...")
        subprocess.run(["git", "push"], cwd=destination_repo_path, check=True)

        print("[SUCCESS] Changes pushed to the .github repository.")
    except subprocess.CalledProcessError as e:
        print(
            f"[ERROR] Git command failed with exit code {e.returncode}. "
            "Check your Git credentials, remote config, or untracked files."
        )


def sync_production_artifacts(push_changes=True):
    """Handles production artifacts sync and optional git operations."""
    original_dir = os.getcwd()
    home_dir = os.path.abspath("..")

    target_folders = {
        "VSDSquadron_FM": "../VSDSquadron_FM",
        "VSDSquadron_Mini": "../VSDSquadron_Mini",
        "VSDSquadron_Pro": "../VSDSquadron_Pro",
        "VSDSquadron_SKY130": "../VSDSquadron_SKY130",
        "VSDSquadron_Ultra": "../VSDSquadron_Ultra",
        "VSDSQuadron_FM_Kit": "../VSDSQuadron_FM_Kit",
    }

    source_folders = {
        "VSDSquadron_FM": "../../PCB_VSDSquadron_FM/squadron_FM/production",
        "VSDSquadron_Mini": "../../PCB_VSDSquadron_Mini/squadron_mini/production",
        "VSDSquadron_Pro": "../../PCB_VSDSquadron_Pro/squadron_pro/production",
        "VSDSquadron_SKY130": "../../PCB_VSDSquadron_SKY130/squadron_sky130/production",
        "VSDSquadron_Ultra": "../../PCB_VSDSquadron_Ultra/squadron_ultra/production",
        "VSDSQuadron_FM_Kit": r"C:\Users\yatha\Desktop\VSD\hardware\PCB_FPGA_KIT\PCB_FPGA_KIT\production",
    }

    for key in target_folders:
        target = target_folders[key]
        source = source_folders[key]

        if os.path.exists(target):
            clear_files(target)

        if os.path.exists(source):
            copy_files(source, target)

    allowed_dirs = {os.path.abspath(path) for path in target_folders.values()}

    for entry in os.listdir(home_dir):
        entry_path = os.path.join(home_dir, entry)
        if not os.path.isdir(entry_path):
            continue

        if entry == "_scripts":
            continue

        if not (entry.startswith("VSDSquadron") or entry.startswith("VSDSQuadron")):
            continue

        if os.path.abspath(entry_path) in allowed_dirs:
            continue

        print(f"[INFO] Removing obsolete folder: {entry_path}")
        shutil.rmtree(entry_path)

    if push_changes:
        os.chdir(home_dir)
        try:
            subprocess.run(["git", "add", "."], check=True)

            status = subprocess.run(
                ["git", "status", "--porcelain"],
                check=True,
                capture_output=True,
                text=True,
            )

            if not status.stdout.strip():
                print("[INFO] No production changes to commit; skipping push.")
            else:
                subprocess.run(
                    ["git", "commit", "-m", "Updated production folders"],
                    check=True,
                )
                subprocess.run(["git", "push"], check=True)
        finally:
            os.chdir(original_dir)

    print("Production artifact sync complete.")


def main():
    parser = argparse.ArgumentParser(
        description="Clear/copy production files and update .github profile assets."
    )
    parser.add_argument(
        "--no-push-production",
        action="store_true",
        help="Skip git push for production artifact sync.",
    )
    parser.add_argument(
        "--no-push-profile",
        action="store_true",
        help="Skip git push for the .github profile repository.",
    )
    parser.add_argument(
        "--skip-production",
        action="store_true",
        help="Skip syncing hardware production artifacts.",
    )
    parser.add_argument(
        "--skip-profile",
        action="store_true",
        help="Skip updating the .github profile README and images.",
    )
    parser.add_argument(
        "--profile-readme",
        default=os.path.join(os.path.dirname(__file__), "..", "README.md"),
        help="Path to the source README whose content/images should be copied.",
    )
    parser.add_argument(
        "--profile-repo",
        default=os.path.join(os.path.dirname(__file__), "..", "..", ".github"),
        help="Path to the destination .github repository.",
    )
    parser.add_argument(
        "--profile-subdir",
        default="profile",
        help="Destination subdirectory within the .github repo (default: profile).",
    )
    args = parser.parse_args()

    if not args.skip_production:
        sync_production_artifacts(push_changes=not args.no_push_production)
    else:
        print("Skipping production artifact sync.")

    if not args.skip_profile:
        copy_readme_and_images_into_profile(
            source_readme_path=args.profile_readme,
            destination_repo_path=args.profile_repo,
            readme_destination_subdir=args.profile_subdir,
            push_changes=not args.no_push_profile,
        )
    else:
        print("Skipping profile README sync.")

    print("Done.")


if __name__ == "__main__":
    main()
