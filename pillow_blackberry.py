from PIL import Image, ImageEnhance

image = Image.open('/Users/pankaj.basnal/repos/DPED/visual_results/blackberry_orig__DSC1037_enhanced.png')

red, green, blue = image.split()

# green = ImageEnhance.Brightness(green).enhance(0.9)
# red = ImageEnhance.Brightness(red).enhance(0.95)
blue = ImageEnhance.Brightness(blue).enhance(1.1)

new_image = Image.merge("RGB", (red, green, blue))
# new_image.save('new_image.jpg')
image.show()
# new_image = ImageEnhance.Sharpness(new_image).enhance(0.8)
new_image = ImageEnhance.Brightness(new_image).enhance(1.1)
new_image.show()
print(new_image.mode) # Output: RGB
