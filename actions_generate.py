#!/usr/bin/env python3
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
FONT_BOLD_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCRIPT_DIR = Path(__file__).parent
BASE_END = SCRIPT_DIR / "base_end.png"
BASE_EVENT = SCRIPT_DIR / "base_event.png"

sm, sd, em, ed = map(int, sys.argv[1:5])

# 기획전 종료
base = Image.open(BASE_END).convert("RGB")
font = ImageFont.truetype(FONT_PATH, 100)
text = f"{sm}.{sd} ~ {em}.{ed}"
frame = base.copy()
draw = ImageDraw.Draw(frame)
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
draw.text((429 - tw//2, 827 - th//2 - bbox[1]), text, fill=(253,253,253), font=font)
out = SCRIPT_DIR / "gifs"
out.mkdir(exist_ok=True)
frame.save(out / "기획전_종료.gif", save_all=True, append_images=[base.copy()], duration=500, loop=0)

# 안진 기획전
base2 = Image.open(BASE_EVENT).convert("RGB")
font2 = ImageFont.truetype(FONT_PATH, 55)
text2 = f"{sm}월 {sd}일 ~ {em}월 {ed}일"
frame2 = base2.copy()
draw2 = ImageDraw.Draw(frame2)
bbox2 = draw2.textbbox((0, 0), text2, font=font2)
tw2, th2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
draw2.text((432 - tw2//2, 850 - th2//2 - bbox2[1]), text2, fill=(253,253,253), font=font2)
frame2.save(out / "안진_기획전.gif", save_all=True, append_images=[base2.copy()], duration=500, loop=0)

print(f"✅ {sm}.{sd} ~ {em}.{ed} 생성 완료")
