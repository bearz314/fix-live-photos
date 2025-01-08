import json
import os
import subprocess
from typing import Any, Dict, List, Tuple

# Dependencies: homebrew exiftool

def main():
    # This script will overwrite the files!

    # Path to directory that contains IMG_xxxx.HEIC and IMG_xxxx.mov files
    input_dir_path  = "/path/to/dir/"

    print(f"Get metadata for {input_dir_path}")
    metadatas = get_metadatas(path=input_dir_path)

    count_actual_live_videos = 0
    count_likely_live_videos = 0
    count_restored_live_videos = 0

    for metadata in metadatas:
        if not is_video(metadata=metadata):
            continue

        if has_contentIdentifier(metadata=metadata):
            count_actual_live_videos += 1
            continue

        # Video file but not a live video

        live_pair_found, photo_path, video_path = find_live_pair(video_metadata=metadata)
        if not live_pair_found:
            continue
        
        # Video file is likely a live video
        count_likely_live_videos += 1
        print(f"Found: {metadata.get('SourceFile')}")

        # Copy ContentIdentifier
        if copy_contentIdentifier_photo_to_video(src_path=photo_path, dst_path=video_path):
            count_restored_live_videos += 1
            print(f"Done: {video_path}")

    print(f"Proper live photos:   {count_actual_live_videos}")
    print(f"Likely live photos:   {count_likely_live_videos}")
    print(f"Restored live photos: {count_restored_live_videos}")


def get_metadatas(path: str) -> List[Dict[str, Any]]:

    # Exiftool on directory, json output, consistent machine readable format, file size in bytes
    command = ["exiftool", "-json", "-n", "-FileSize#", "-All", path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Check for errors
    if result.returncode != 0:
        raise Exception(f"Exiftool error: {result.stderr}")
    
    # Parse the JSON output
    try:
        return json.loads(result.stdout)
    except:
        return []

def is_video(metadata: Dict[str, Any]) -> bool:
    return metadata.get("MIMEType","").startswith("video/")

def has_contentIdentifier(metadata: Dict[str, Any]) -> bool:
    return metadata.get("ContentIdentifier") is not None

def find_live_pair(video_metadata: Dict[str, Any]) -> Tuple[bool, str, str]:
    # check file extension is .mov (case sensitive: lower)
    is_extension_lowercase = video_metadata.get('FileName',"").endswith(".mov")

    # check duration is short
    duration_str = video_metadata.get('Duration',"100")
    is_duration_short = float(duration_str) < 5

    # check corresponding photo exists (case sensitive: upper)
    base_video_name = os.path.splitext(video_metadata.get('FileName', ""))[0]  # Extract the base name (e.g., IMG_0253)

    video_path = video_metadata.get('SourceFile')
    dir_name = video_metadata.get('Directory')
    corresponding_photo_name = f"{base_video_name}.HEIC"
    corresponding_photo_path = os.path.join(dir_name, corresponding_photo_name)
    files_in_dir = os.listdir(dir_name)
    is_photo_exist = corresponding_photo_name in files_in_dir

    if is_extension_lowercase and is_duration_short and is_photo_exist:
        return (True, corresponding_photo_path, video_path)
    
    return (False, None, None)
    

def copy_contentIdentifier_photo_to_video(src_path: str, dst_path: str) -> bool:
    # check source ContentIdentifier
    photo_metadata = get_metadatas(src_path)[0]
    if not has_contentIdentifier(metadata=photo_metadata):
        return False
    
    # copy ContentIdentifier to destination
    command = ["exiftool", "-overwrite_original", "-TagsFromFile", src_path, "-Keys:ContentIdentifier<Apple:ContentIdentifier", dst_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Check for errors
    if result.returncode != 0:
        raise Exception(f"Exiftool error: {result.stderr}")
    
    return True


if __name__ == "__main__":
    main()