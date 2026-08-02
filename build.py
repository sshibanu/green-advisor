#!/usr/bin/env python3
"""shell.html（UI）と content/chNN.json（教材データ）から index.html を生成する。

    python3 build.py

content/ の JSON を編集したら、このスクリプトを実行して index.html を作り直す。
"""
import json, glob, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def main():
    files = sorted(glob.glob(os.path.join(ROOT, "content", "ch*.json")))
    if not files:
        sys.exit("content/ に章データが見つかりません")

    chapters = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            chapters.append(json.load(fh))
    chapters.sort(key=lambda d: d["id"])

    # 最低限の整合チェック
    for ch in chapters:
        for q in ch["quiz"]:
            if q["type"] == "mc":
                assert len(q["choices"]) == 3, f"第{ch['id']}章: 三択の選択肢が3つでない"
                assert q["a"] in (0, 1, 2), f"第{ch['id']}章: 正解インデックスが不正"
            else:
                assert isinstance(q["a"], bool), f"第{ch['id']}章: ○×の正解が真偽値でない"

    data = json.dumps(chapters, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(ROOT, "shell.html"), encoding="utf-8") as fh:
        shell = fh.read()
    if "__DATA__" not in shell:
        sys.exit("shell.html に __DATA__ プレースホルダがありません")

    out = shell.replace("__DATA__", data)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(out)

    n_sec = sum(len(c["sections"]) for c in chapters)
    n_q = sum(len(c["quiz"]) for c in chapters)
    print(f"index.html を生成しました: {len(chapters)}章 / {n_sec}レッスン / {n_q}問 "
          f"({len(out.encode()) // 1024} KB)")

if __name__ == "__main__":
    main()
