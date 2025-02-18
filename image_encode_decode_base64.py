import base64
import io

from PIL import Image


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def decode_image(encoded_string: str) -> Image:
    image_data = base64.b64decode(encoded_string)
    return Image.open(io.BytesIO(image_data))


if __name__ == "__main__":
    # 8 by 8 grid image
    encoded_string = "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII="
    # 10 by 10 red
    # encoded_string = "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8z8BQz0AEYBxVSF+FABJADveWkH6oAAAAAElFTkSuQmCC="
    decoded_image = decode_image(encoded_string)
    print("decoded_image.size", decoded_image.size)
    decoded_image.save("decoded_image.png")
