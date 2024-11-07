import argparse
import os
import json

import tqdm

import google.generativeai as genai

import dotenv

dotenv.load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_GEMINI_API_KEY"])


def main(file_path: str, size: int):
    with open(file_path, "r") as f:
        data = json.load(f)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={os.environ['GOOGLE_GEMINI_API_KEY']}"

    embeddings = list()

    for i, video in tqdm.tqdm(enumerate(data), desc="Generating embeddings"):
        output = genai.embed_content(
            model="models/text-embedding-004",
            content=[ t for t in video["transcription"] ],
            output_dimensionality=size
        )

        embeddings.append({
            "video_id": video["video_id"],
            "embeddings": output["embedding"]
        })

    print(json.dumps(embeddings, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("file_path", help="File containing transcriptions.")
    parser.add_argument("size", type=int, help="Embedding size.")

    args = parser.parse_args()

    main(args.file_path, args.size)
