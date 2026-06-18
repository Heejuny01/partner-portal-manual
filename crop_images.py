"""Re-extract and crop manual pages: detect screenshot frame, trim empty space."""
from pathlib import Path
import fitz
from PIL import Image

PDF = Path(r"c:\Users\pc001\Desktop\공사관리시스템_협력사포탈_사용자매뉴얼_v0.1.pdf")
OUT = Path(__file__).parent / "images"

# page-02는 PDF가 아닌 실제 포탈(b2b.hwenc.com) 캡처 사용
SKIP_PAGE_INDEXES = {1}


def is_dark(px, x, y, w, h):
    if x < 0 or y < 0 or x >= w or y >= h:
        return False
    r, g, b = px[x, y]
    return r < 60 and g < 60 and b < 60


def find_screenshot_box(im: Image.Image) -> tuple[int, int, int, int]:
    """PDF 매뉴얼의 스크린샷 검은 테두리 안쪽 영역을 찾는다."""
    w, h = im.size
    px = im.load()

    top = 200
    for y in range(150, 280):
        if sum(1 for x in range(5, 950) if is_dark(px, x, y, w, h)) > 400:
            top = y
            break

    bottom = h - 40
    for y in range(h - 80, top, -1):
        if sum(1 for x in range(5, 950) if is_dark(px, x, y, w, h)) > 400:
            bottom = y
            break

    left = 5
    for x in range(3, 30):
        if sum(1 for y in range(top, bottom) if is_dark(px, x, y, w, h)) > (bottom - top) * 0.5:
            left = x
            break

    # 기능설명 열 앞의 첫 번째 세로 테두리 (오른쪽 끝이 아닌 스크린샷 우측선)
    right = 899
    for x in range(860, 980):
        if sum(1 for y in range(top, bottom) if is_dark(px, x, y, w, h)) > (bottom - top) * 0.5:
            right = x
            break

    return left + 2, top + 2, right - 1, bottom - 1


def trim_empty_bottom(im: Image.Image, margin: int = 4) -> Image.Image:
    """하단의 빈 흰색·단색 여백을 제거한다."""
    w, h = im.size
    px = im.load()

    def row_score(y: int) -> int:
        samples = [px[x, y] for x in range(0, w, max(1, w // 120))]
        avg = tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
        diff = sum(
            abs(px[x, y][0] - avg[0]) + abs(px[x, y][1] - avg[1]) + abs(px[x, y][2] - avg[2])
            for x in range(0, w, max(1, w // 80))
        )
        return diff

    last_content = 0
    for y in range(h):
        if row_score(y) > 35:
            last_content = y

    bottom = min(h, last_content + margin + 1)
    if bottom >= h - 2:
        return im
    return im.crop((0, 0, w, bottom))


def render_page(doc, index: int) -> Image.Image:
    page = doc[index]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def crop_page(im: Image.Image) -> Image.Image:
    box = find_screenshot_box(im)
    cropped = im.crop(box)
    return trim_empty_bottom(cropped)


def main():
    OUT.mkdir(exist_ok=True)
    doc = fitz.open(PDF)
    for i in range(len(doc)):
        if i in SKIP_PAGE_INDEXES:
            print(f"page-{i + 1:02d}.png skipped (live portal capture)")
            continue
        im = render_page(doc, i)
        result = crop_page(im)
        out = OUT / f"page-{i + 1:02d}.png"
        result.save(out, optimize=True)
        print(out.name, result.size)
    doc.close()


if __name__ == "__main__":
    main()
