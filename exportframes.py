import cv2
import os
import argparse
from datetime import timedelta

def extract_frames(video_path, output_dir, fps=3):
    """
    Extract frames from a video at a specified rate (frames per second).
    
    Args:
        video_path (str): Path to the input video file
        output_dir (str): Directory to save extracted frames
        fps (int): Number of frames to extract per second
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Get video properties
    video_fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / video_fps
    
    # Calculate frame interval
    frame_interval = int(video_fps / fps)
    
    # Print video information
    print(f"Video: {video_path}")
    print(f"Duration: {timedelta(seconds=duration)}")
    print(f"Original FPS: {video_fps}")
    print(f"Extracting at {fps} FPS (every {frame_interval} frames)")
    print(f"Output directory: {output_dir}")
    
    count = 0
    frame_count = 0
    saved_count = 0
    
    while True:
        success, frame = video.read()
        if not success:
            break
            
        # Save frame if it's at the right interval
        if count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{saved_count:05d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
            
            # Print progress every 10 frames
            if saved_count % 10 == 0:
                print(f"Saved {saved_count} frames...")
                
        count += 1
        frame_count += 1
    
    video.release()
    print(f"Extraction complete! Saved {saved_count} frames from {frame_count} total frames.")

if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Extract frames from a video at a specified rate.")
    parser.add_argument("video_path", help="Path to the input video file")
    parser.add_argument("--output_dir", default="extracted_frames", help="Directory to save extracted frames")
    parser.add_argument("--fps", type=int, default=3, help="Number of frames to extract per second")
    
    args = parser.parse_args()
    
    # Extract frames
    extract_frames(args.video_path, args.output_dir, args.fps)