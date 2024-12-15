import cv2

input_image = 'c66e4e19-55ab-4447-a2ea-2373e7fcabef.jfif'
output_image = input_image.split('.')[0] + '.png'
image = cv2.imread(input_image)
cv2.imwrite(output_image, image)
