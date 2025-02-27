from PIL import Image

img = Image.new("RGBA" , (1,1) ,(0,0,0,0))
img.save('pixel.png')