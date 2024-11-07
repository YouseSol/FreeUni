import argparse
import json
import traceback
import sys

import tqdm

import youtube_transcript_api as yta


def main(file_path: str):
    with open(file_path, "r") as f:
        data = json.load(f)

    transcriptions = list()

    for video in tqdm.tqdm(data):
        video_id = video["id"]["videoId"]

        try:
            transcription_data = yta.YouTubeTranscriptApi.get_transcript(video_id, languages=('pt', ))

            output_data = {
                "channel": video["snippet"]["channelTitle"],
                "channel_id": video["snippet"]["channelId"],
                "video_id": video_id,
                "date": video["snippet"]["publishTime"],
                "transcription": [ t["text"] for t in transcription_data ],
                "language": "pt"
            }

            transcriptions.append(output_data)
        except Exception as e:
            try:
                transcription_data = yta.YouTubeTranscriptApi.get_transcript(video_id, languages=('en', ))

                output_data = {
                    "channel": video["snippet"]["channelTitle"],
                    "channel_id": video["snippet"]["channelId"],
                    "video_id": video_id,
                    "date": video["snippet"]["publishTime"],
                    "transcription": [ t["text"] for t in transcription_data ],
                    "language": "en"
                }

                transcriptions.append(output_data)
            except Exception as e:
                print(traceback.format_exc(), file=sys.stderr)

    print(json.dumps(transcriptions, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("file_path", help="File containing data from Youtube Data API v3.")

    args = parser.parse_args()

    main(args.file_path)
