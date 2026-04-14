#!/usr/bin/env python3
"""
🎯 스마트스토어 이벤트 날짜 GIF 자동 생성 & GitHub Pages 업로드
================================================================

사용법:
    python update_event.py 4 15 4 21
    → 시작일: 4월 15일, 종료일: 4월 21일
    → GIF 생성 + GitHub 자동 push + 상세페이지 자동 반영!

최초 설정 후에는 이 명령어 하나로 모든 게 끝납니다.
"""

import sys
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ============================================================
# 🔧 설정 - 본인 환경에 맞게 수정하세요
# ============================================================

# GitHub 저장소 로컬 경로 (git clone한 폴더)
REPO_DIR = Path.home() / "store-event-gifs"

# GIF가 저장될 저장소 내 폴더
GIF_FOLDER = "gifs"

# 폰트 설정 (macOS)
FONT_BLACK = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FONT_BOLD = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

# 위 폰트가 없을 경우 대체 경로 (Noto Sans 설치 시)
FONT_BLACK_ALT = "/Users/chojoongchan/Library/Fonts/NotoSansCJKkr-Black.otf"
FONT_BOLD_ALT = "/Library/Fonts/NotoSansCJKkr-Bold.otf"

# 베이스 이미지 경로 (이 스크립트와 같은 폴더)
SCRIPT_DIR = Path(__file__).parent
BASE_END_PATH = SCRIPT_DIR / "base_end.png"
BASE_EVENT_PATH = SCRIPT_DIR / "base_event.png"

# GIF 설정
BLINK_DURATION = 500  # 깜빡임 속도 (ms)


# ============================================================
# 폰트 로딩
# ============================================================

def load_font(primary, alt, size):
    """폰트 로딩 (기본 → 대체 순서로 시도)"""
    for path in [primary, alt]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    print("⚠️  한글 폰트를 찾을 수 없습니다.")
    print("   아래 명령어로 Noto Sans CJK를 설치하세요:")
    print("   brew install font-noto-sans-cjk-kr")
    sys.exit(1)


# ============================================================
# GIF 생성
# ============================================================

def generate_end_gif(sm, sd, em, ed, output_path):
    """기획전 종료 안내 GIF (어두운 배경 + 빨간 박스)"""
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
    """기획전 진행 안내 GIF (밝은 배경 + 검은 박스)"""
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


# ============================================================
# GitHub Push
# ============================================================

def git_push(sm, sd, em, ed):
    """변경된 GIF를 GitHub에 push"""
    os.chdir(REPO_DIR)
    msg = f"이벤트 날짜 변경: {sm}.{sd} ~ {em}.{ed}"

    for cmd in [["git", "add", "."],
                ["git", "commit", "-m", msg],
                ["git", "push"]]:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 and "nothing to commit" not in r.stdout:
            print(f"  ⚠️  git 오류: {r.stderr.strip()}")
            return False
    print(f"  📤 GitHub push 완료")
    return True


# ============================================================
# 메인
# ============================================================

def main():
    if len(sys.argv) == 5:
        sm, sd, em, ed = map(int, sys.argv[1:5])
    elif len(sys.argv) == 1:
        print("\n📅 이벤트 날짜를 입력하세요:")
        sm = int(input("  시작 월: "))
        sd = int(input("  시작 일: "))
        em = int(input("  종료 월: "))
        ed = int(input("  종료 일: "))
    else:
        print("사용법: python update_event.py [시작월] [시작일] [종료월] [종료일]")
        print("  예시: python update_event.py 4 22 4 28")
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
