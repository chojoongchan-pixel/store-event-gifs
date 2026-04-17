#!/usr/bin/env python3
"""
🎯 스마트스토어 이벤트 날짜 GIF 자동 생성 & GitHub Pages 업로드

사용법:
    python3 update_event.py 4 15       → 종료일만 입력 (시작일 = 7일 전 자동 계산)
    python3 update_event.py 4 9 4 15   → 시작일~종료일 직접 입력
    python3 update_event.py            → 대화형 입력
"""

import sys
import os
import subprocess
from pathlib import Path
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont

REPO_DIR = Path.home() / "store-event-gifs"
GIF_FOLDER = "gifs"
FONT_BLACK = "/Users/chojoongchan/Library/Fonts/NotoSansCJKkr-Black.otf"
FONT_BOLD = "/Users/chojoongchan/Library/Fonts/NotoSansCJKkr-Black.otf"
FONT_BLACK_ALT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FONT_BOLD_ALT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
SCRIPT_DIR = Path(__file__).parent
BASE_END_PATH = SCRIPT_DIR / "base_end.png"
BASE_EVENT_PATH = SCRIPT_DIR / "base_event.png"
BLINK_DURATION = 500

def load_font(primary, alt, size):
    for path in [primary, alt]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    print("⚠️  한글 폰트를 찾을 수 없습니다.")
    sys.exit(1)

def generate_end_gif(sm, sd, em, ed, output_path):
    base = Image.open(BASE_END_PATH).convert("RGB")
    font = load_font(FONT_BLACK, FONT_BLACK_ALT, 100)
    date_text = f"{sm}.{sd} ~ {em}.{ed}"
    frame = base.copy()
    draw = ImageDraw.Draw(frame)
    bbox = draw.textbbox((0, 0), date_text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((429 - tw // 2, 827 - th // 2 - bbox[1]),
              date_text, fill=(253, 253, 253), font=font)
    frame.save(output_path, save_all=True, append_images=[base.copy()],
               duration=BLINK_DURATION, loop=0)
    print(f"  ✅ 기획전_종료.gif")

def generate_event_gif(sm, sd, em, ed, output_path):
    base = Image.open(BASE_EVENT_PATH).convert("RGB")
    font = load_font(FONT_BOLD, FONT_BOLD_ALT, 55)
    date_text = f"{sm}월 {sd}일 ~ {em}월 {ed}일"
    frame = base.copy()
    draw = ImageDraw.Draw(frame)
    bbox = draw.textbbox((0, 0), date_text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((432 - tw // 2, 850 - th // 2 - bbox[1]),
              date_text, fill=(253, 253, 253), font=font)
    frame.save(output_path, save_all=True, append_images=[base.copy()],
               duration=BLINK_DURATION, loop=0)
    print(f"  ✅ 안진_기획전.gif")

def git_push(sm, sd, em, ed):
    os.chdir(REPO_DIR)
    msg = f"이벤트 날짜 변경: {sm}.{sd} ~ {em}.{ed}"
    for cmd in [["git", "add", "."],
                ["git", "commit", "-m", msg],
                ["git", "pull", "--rebase"],
                ["git", "push"]]:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 and "nothing to commit" not in r.stdout:
            print(f"  ⚠️  git 오류: {r.stderr.strip()}")
            return False
    print(f"  📤 GitHub push 완료")
    return True

def main():
    if len(sys.argv) == 3:
        # 종료일만 입력 → 시작일 자동 계산 (7일 전)
        em, ed = int(sys.argv[1]), int(sys.argv[2])
        end_date = date(date.today().year, em, ed)
        start_date = end_date - timedelta(days=6)
        sm, sd = start_date.month, start_date.day
    elif len(sys.argv) == 5:
        sm, sd, em, ed = map(int, sys.argv[1:5])
    elif len(sys.argv) == 1:
        print("\n📅 이벤트 종료일을 입력하세요 (시작일은 7일 전 자동 계산):")
        em = int(input("  종료 월: "))
        ed = int(input("  종료 일: "))
        end_date = date(date.today().year, em, ed)
        start_date = end_date - timedelta(days=6)
        sm, sd = start_date.month, start_date.day
    else:
        print("사용법:")
        print("  python3 update_event.py 4 15         (종료일만, 시작일 자동)")
        print("  python3 update_event.py 4 9 4 15     (시작일~종료일 직접)")
        sys.exit(1)

    print(f"\n🎯 이벤트 기간: {sm}월 {sd}일 ~ {em}월 {ed}일")
    print("=" * 50)

    gif_dir = REPO_DIR / GIF_FOLDER
    gif_dir.mkdir(parents=True, exist_ok=True)

    print("\n📦 GIF 생성 중...")
    generate_end_gif(sm, sd, em, ed, gif_dir / "기획전_종료.gif")
    generate_event_gif(sm, sd, em, ed, gif_dir / "안진_기획전.gif")

    print("\n☁️  GitHub 업로드 중...")
    git_push(sm, sd, em, ed)

    print(f"\n{'=' * 50}")
    print("🎉 완료! 1~2분 후 상세페이지에 자동 반영됩니다.\n")

if __name__ == "__main__":
    main()
