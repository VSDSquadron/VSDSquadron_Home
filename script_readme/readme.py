import os
import shutil
import argparse
import subprocess

def clear_files(target_folder):
    """Deletes existing .jpg and .pdf files from the target folder."""
    for ext in ['.jpg', '.pdf']:
        for file in os.listdir(target_folder):
            if file.endswith(ext):
                os.remove(os.path.join(target_folder, file))


def copy_files(source_folder, target_folder):
    """Copies .jpg, .pdf, and bom.csv files from source to target folder."""
    for ext in ['.jpg', '.pdf', 'bom.csv']:
        src_path = os.path.join(source_folder, ext)
        if os.path.exists(source_folder):
            shutil.copytree(source_folder, target_folder, dirs_exist_ok=True, ignore=lambda _, files: [f for f in files if not f.endswith(ext)])

def main(no_push):
    """Main function to handle file management and optional git operations."""
    original_dir = os.getcwd()

    # Define target folders (one level up)
    target_folders = {
        "VSDSquadron_FM": "../VSDSquadron_FM",
        "VSDSquadron_Mini": "../VSDSquadron_Mini",
        "VSDSquadron_Pro": "../VSDSquadron_Pro",
        "VSDSquadron_S3": "../VSDSquadron_S3",
        "VSDSquadron_SKY130": "../VSDSquadron_SKY130",
        "VSDSquadron_Ultra": "../VSDSquadron_Ultra",
    }

    # Define source folders (two levels up)
    source_folders = {
        "VSDSquadron_FM": "../../PCB_VSDSquadron_FM/squadron_FM/production",
        "VSDSquadron_Mini": "../../PCB_VSDSquadron_Mini/squadron_mini/production",
        "VSDSquadron_Pro": "../../PCB_VSDSquadron_Pro/squadron_pro/production",
        "VSDSquadron_S3": "../../PCB_VSDSquadron_S3/squadron_s3/production",
        "VSDSquadron_SKY130": "../../PCB_VSDSquadron_SKY130/squadron_sky130/production",
        "VSDSquadron_Ultra": "../../PCB_VSDSquadron_Ultra/squadron_ultra/production",
    }

    # Clear and copy files
    for key in target_folders:
        target = target_folders[key]
        source = source_folders[key]
        
        if os.path.exists(target):
            clear_files(target)
        
        if os.path.exists(source):
            copy_files(source, target)

    # Git operations
    if not no_push:
        os.chdir("..")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Updated production folders"], check=True)
        subprocess.run(["git", "push"], check=True)
        os.chdir(original_dir)
    
    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clear and copy production files, with optional Git push.")
    parser.add_argument("--no-push", action="store_true", help="Skip the Git push step.")
    args = parser.parse_args()
    
    main(args.no_push)
