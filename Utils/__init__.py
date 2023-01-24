from PIL import Image
from F import OS


# Open the image file


# Save the image in JPEG format
def convert_image_to_jpg(filePath):
    newFile = OS.remove_file_ext(filePath)
    image = Image.open(filePath)
    image = image.convert("RGB")
    image.save(f"{newFile}.jpg", "JPEG")


cwd = "/Users/chazzromeo/ChazzCoin/Tiffany-Alpha-0/AI/DETRresnetObjectDetection"
image_test_path = f"{cwd}/testImage.png"
new_image_test_path = f"{cwd}/testImage.jpg"
convert_image_to_jpg(image_test_path)