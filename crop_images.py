"""Re-extract and crop manual pages: system UI + 기능설명 only."""
from pathlib import Path
import fitz
from PIL import Image, ImageDraw

PDF = Path(r"c:\Users\pc001\Desktop\공사관리시스템_협력사포탈_사용자매뉴얼_v0.1.pdf")
OUT = Path(__file__).parent / "images"

# 2x render -> 1560x1080
TOP = 142          # UF 헤더 + 메뉴/개요/비고/작성일 행 제거
BOTTOM = 1038      # 페이지 번호 제거
FUNC_COL = 920     # 기능설명 열 시작 (대략)
MASK_UNTIL = 208   # 데이터 행(메뉴·개요 등) 가리는 높이


def render_page(doc, index: int) -> Image.Image:
    page = doc[index]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def crop_page(im: Image.Image) -> Image.Image:
    w, h = im.size
    cropped = im.crop((0, TOP, w, min(BOTTOM, h)))
    draw = ImageDraw.Draw(cropped)
    # 상단 데이터 행의 메뉴·개요·비고·작성일 영역만 흰색으로 가림 (기능설명 열은 유지)
    mask_h = MASK_UNTIL - TOP
    if mask_h > 0:
        draw.rectangle((0, 0, FUNC_COL, mask_h), fill=(255, 255, 255))
    return cropped


def main():
    OUT.mkdir(exist_ok=True)
    doc = fitz.open(PDF)
    for i in range(len(doc)):
        im = render_page(doc, i)
        result = crop_page(im)
        out = OUT / f"page-{i + 1:02d}.png"
        result.save(out, optimize=True)
        print(out.name, result.size)
    doc.close()


if __name__ == "__main__":
    main()
