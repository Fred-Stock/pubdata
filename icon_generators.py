from PIL import Image, ImageDraw, ImageFont

def create_pdf_icon(filename="pdf_icon.png"):
    """Create a PDF icon with a clean design."""
    size = (128, 128)
    img = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Draw a paper with a folded corner
    draw.rectangle([16, 8, 112, 120], fill=(255, 255, 255), outline=(200, 0, 0), width=4)
    draw.polygon([(112, 8), (96, 8), (112, 24)], fill=(200, 0, 0))

    # Draw bold "PDF" text
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()

    draw.text((24, 70), "PDF", fill=(200, 0, 0), font=font)

    img.save(filename)
    print(f"PDF icon saved as {filename}")


def create_code_icon(filename="code_icon.png"):
    """Create a code icon with a terminal-like appearance."""
    size = (128, 128)
    img = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Draw a terminal-like window
    #draw.rectangle([8, 24, 120, 104], fill=(50, 50, 50), outline=(0, 0, 0), width=4)
    draw.rectangle([12, 12, 116, 116], fill=(50, 50, 50), outline=(0, 0, 0), width=4)

    # Draw the '>' symbol and underscore cursor
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
    except:
        font = ImageFont.load_default()

    draw.text((20, 54), ">", fill=(0, 255, 0), font=font)
    draw.text((56, 54), "_", fill=(0, 255, 0), font=font)

    img.save(filename)
    print(f"Code icon saved as {filename}")


if __name__ == "__main__":
    create_pdf_icon("pdf_icon.png")
    create_code_icon("code_icon.png")
