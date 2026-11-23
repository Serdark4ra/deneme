#!/usr/bin/env python3
"""Basit bir not defteri."""

import json
import sys
from pathlib import Path

STORE = Path(__file__).with_name("notes.json")


def load_notes():
    if not STORE.exists():
        return []
    return json.loads(STORE.read_text(encoding="utf-8"))


def save_notes(notes):
    STORE.write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add_note(text):
    notes = load_notes()
    notes.append({"text": text, "done": False})
    save_notes(notes)
    print(f"Eklendi: {text}")


def list_notes():
    notes = load_notes()
    if not notes:
        print("Henüz not yok.")
        return
    for index, note in enumerate(notes, start=1):
        mark = "x" if note["done"] else " "
        print(f"{index}. [{mark}] {note['text']}")


def mark_done(raw_index):
    try:
        index = int(raw_index)
    except ValueError:
        print("Not numarası bir tam sayı olmalı.")
        return 1
    notes = load_notes()
    if index < 1 or index > len(notes):
        print("Böyle bir not yok.")
        return 1
    notes[index - 1]["done"] = True
    save_notes(notes)
    print(f"Tamamlandı: {notes[index - 1]['text']}")
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] not in {"add", "list", "done"}:
        print("Kullanım: notes.py add <metin> | list | done <numara>")
        return 1
    if argv[1] == "add":
        if len(argv) < 3:
            print("Eklenecek metni yaz.")
            return 1
        add_note(" ".join(argv[2:]))
        return 0
    if argv[1] == "done":
        if len(argv) != 3:
            print("Kullanım: notes.py done <numara>")
            return 1
        return mark_done(argv[2])
    list_notes()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
