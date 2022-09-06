import os
import glob
import argparse
from tqdm import tqdm
from imageio import mimread

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="/home/brianw0924/SN850/vox2_mp4/train")

    parser.add_argument("--record_broken_videos", action="store_true")
    parser.add_argument("--remove_broken_videos", action="store_true")
    parser.add_argument("--broken_videos_txtPath", type=str, default="broken_videos.txt")

    parser.add_argument("--remove_empty_folders", action="store_true")

    parser.add_argument("--filter_id", action="store_true")
    parser.add_argument("--filter_id_txtPath", type=str, default="filtered_id.txt")

    args = parser.parse_args()
    return args

def record_broken_videos(data_dir: str, txtPath: str):
        with open(txtPath, 'w') as f:
                f.write("broken_video_path\n")

        for _id in tqdm(glob.glob(f"{data_dir}/*")):
                for video_id in glob.glob(f"{_id}/*"):
                        for video_path in glob.glob(f"{video_id}/*"):
                                try:
                                        _ = mimread(video_path, memtest=False)
                                except Exception as e:
                                        with open(txtPath, 'a') as f:
                                                f.write(f"{video_path}\n")

def remove_broken_videos(txtPath: str):
        cnt = 0
        with open(txtPath) as f :
                next(f)
                for path in tqdm(f.readlines()):
                        path = path.strip()
                        if os.path.exists(path):
                                os.remove(path)
                                cnt+=1
                                tqdm.write(f"Removed: {path}")

        tqdm.write(f"Removed: {cnt} videos")

def remove_empty_folders(data_dir: str):
        cnt = 0
        for _id in tqdm(glob.glob(f"{data_dir}/*")):
                for v in glob.glob(f"{_id}/*"):
                        if len(os.listdir(v)) == 0:
                                os.rmdir(v)
                                cnt+=1
                                tqdm.write(f"Removed: {v}")
        tqdm.write(f"Removed: {cnt} folders")

def filter_id(txtPath: str, data_dir: str):
        thres = 10
        video_cnt={}

        for _id in tqdm(glob.glob(f"{data_dir}/*")):
                c=0
                for v in glob.glob(f"{_id}/*"):
                        if len(os.listdir(v)) > 0:
                                c+=1
                video_cnt[os.path.basename(_id)] = c

        with open(txtPath, 'w') as f:
                for k, v in sorted(video_cnt.items(), key=lambda x: x[1], reverse=True):
                        if v >= thres:
                                tqdm.write(f"{k},{v}")
                                f.write(f"{k}\n")


if __name__ == "__main__":
        args = get_args()
        if args.record_broken_videos:
                record_broken_videos(args.broken_videos_txtPath, args.data_dir)
        if args.remove_broken_videos:
                remove_broken_videos(args.broken_videos_txtPath)
        if args.remove_empty_folders:
                remove_empty_folders(args.data_dir)
        if args.filter_id:
                filter_id(args.filter_id_txtPath, args.data_dir)