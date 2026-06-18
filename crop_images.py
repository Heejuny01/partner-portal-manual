"""Re-extract and crop manual pages: system UI screenshot only."""
from pathlib import Path
import fitz
from PIL import Image

PDF = Path(r"c:\Users\pc001\Desktop\공사관리시스템_협력사포탈_사용자매뉴얼_v0.1.pdf")
OUT = Path(__file__).parent / "images"

# 2x render -> 1560x1080
CONTENT_TOP = 208   # 메타데이터 표(UF·메뉴·개요·비고·작성일) 아래
BOTTOM = 1038       # 페이지 번호 제거
SYSTEM_RIGHT = 895  # 기능설명 열 제외, 시스템 화면만


def render_page(doc, index: int) -> Image.Image:
    page = doc[index]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def crop_page(im: Image.Image) -> Image.Image:
    w, h = im.size
    return im.crop((0, CONTENT_TOP, SYSTEM_RIGHT, min(BOTTOM, h)))


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
