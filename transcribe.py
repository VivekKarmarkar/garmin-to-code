#!/usr/bin/env python3
"""Transcribe Telegram voice messages (.oga) using OpenAI Whisper API."""

import sys
import os
from openai import OpenAI


def transcribe(file_path: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    with open(file_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
        )
    return result.text


def main():
    if len(sys.argv) < 2:
        # No argument — find most recent .oga in Telegram inbox
        inbox = os.path.expanduser("~/.claude/channels/telegram/inbox")
        if not os.path.isdir(inbox):
            print("No Telegram inbox found.", file=sys.stderr)
            sys.exit(1)
        oga_files = sorted(
            [f for f in os.listdir(inbox) if f.endswith(".oga")],
            reverse=True,
        )
        if not oga_files:
            print("No .oga files in Telegram inbox.", file=sys.stderr)
            sys.exit(1)
        file_path = os.path.join(inbox, oga_files[0])
    else:
        file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    transcript = transcribe(file_path)
    print(transcript)


if __name__ == "__main__":
    main()
