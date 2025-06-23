#!/usr/bin/env python3
import json
import shutil
import glob
import os
from pathlib import Path

def get_user_choice(prompt, options):
    # display menu
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    # get choice
    while True:
        try:
            choice = int(input("\nEnter choice: "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print("Invalid choice, try again")
        except ValueError:
            print("Enter a number")

def cleanup_preprocessing():
    # get all configs - only json files
    config_files = []
    for item in glob.glob('configs/preprocessing_*'):
        if os.path.isfile(item) and item.endswith('.json'):
            config_files.append(item)
    
    config_files = sorted(config_files)
    
    if not config_files:
        print("No preprocessing configs found.")
        # check for bad dir
        if os.path.isdir('configs/preprocessing_config.json'):
            print("\n⚠️  Found directory 'configs/preprocessing_config.json' - this should be removed")
            if input("Remove it? (y/n): ").lower() == 'y':
                shutil.rmtree('configs/preprocessing_config.json')
                print("✓ Removed")
        return
    
    # main menu
    print("="*60)
    print("Preprocessing Cleanup Tool")
    print("="*60)
    
    # action choice
    actions = ["Preview files to delete", "Delete all preprocessing data", "Select specific runs to delete", "Exit"]
    action = get_user_choice("What would you like to do?", actions)
    
    if action == 3:  # exit
        print("Exiting...")
        return
    
    # collect artifacts
    all_clips = []
    all_frames = []
    run_data = {}  # map config to artifacts
    
    # parse configs
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            timestamp = config.get('processing_timestamp', 'unknown')
            run_data[timestamp] = {
                'config': config_file,
                'clip': config.get('clip_path', ''),
                'frames': config.get('frames_dir', ''),
                'method': config.get('preprocessing_method', 'unknown')
            }
            
            if config.get('clip_path'):
                all_clips.append(config['clip_path'])
            if config.get('frames_dir'):
                all_frames.append(config['frames_dir'])
        except Exception as e:
            print(f"Warning: Could not read {config_file}: {e}")
    
    if action == 2:  # select specific
        # show runs
        print("\nAvailable preprocessing runs:")
        timestamps = list(run_data.keys())
        for i, ts in enumerate(timestamps, 1):
            method = run_data[ts]['method']
            print(f"  {i}. {ts} (method: {method})")
        
        # multi select
        print("\nEnter run numbers to delete (comma separated, or 'all'):")
        selection = input().strip()
        
        if selection.lower() == 'all':
            selected_runs = timestamps
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                selected_runs = [timestamps[i] for i in indices if 0 <= i < len(timestamps)]
            except:
                print("Invalid selection")
                return
        
        # filter artifacts
        clips_to_delete = []
        frames_to_delete = []
        configs_to_delete = []
        
        for ts in selected_runs:
            if run_data[ts]['clip']:
                clips_to_delete.append(run_data[ts]['clip'])
            if run_data[ts]['frames']:
                frames_to_delete.append(run_data[ts]['frames'])
            configs_to_delete.append(run_data[ts]['config'])
    
    else:  # delete all
        clips_to_delete = all_clips
        frames_to_delete = all_frames
        configs_to_delete = config_files
    
    # show summary
    print("\n" + "="*60)
    print("Files to process:")
    print("="*60)
    
    print(f"\nClips ({len(clips_to_delete)}):")
    for clip in clips_to_delete:
        exists = "✓" if os.path.exists(clip) else "✗"
        print(f"  {exists} {clip}")
    
    print(f"\nFrame directories ({len(frames_to_delete)}):")
    for frame_dir in frames_to_delete:
        exists = "✓" if os.path.exists(frame_dir) else "✗"
        print(f"  {exists} {frame_dir}")
    
    print(f"\nConfigs ({len(configs_to_delete)}):")
    for config in configs_to_delete:
        exists = "✓" if os.path.exists(config) else "✗"
        print(f"  {exists} {config}")
    
    if action == 0:  # preview only
        print("\n📋 Preview complete (no files deleted)")
        return
    
    # confirm delete
    print("\n⚠️  WARNING: This will permanently delete the files above!")
    confirm = input("Type 'DELETE' to confirm: ").strip()
    
    if confirm != 'DELETE':
        print("Cancelled")
        return
    
    # delete files
    print("\n🗑️  Deleting files...")
    deleted_count = 0
    
    # del clips
    for clip in clips_to_delete:
        if os.path.exists(clip):
            os.remove(clip)
            print(f"✓ Deleted: {clip}")
            deleted_count += 1
    
    # del frames
    for frame_dir in frames_to_delete:
        if os.path.exists(frame_dir):
            shutil.rmtree(frame_dir)
            print(f"✓ Deleted: {frame_dir}")
            deleted_count += 1
    
    # del configs
    for config in configs_to_delete:
        if os.path.exists(config):
            os.remove(config)
            print(f"✓ Deleted: {config}")
            deleted_count += 1
    
    print(f"\n✓ Cleanup complete - deleted {deleted_count} items")

if __name__ == '__main__':
    cleanup_preprocessing()