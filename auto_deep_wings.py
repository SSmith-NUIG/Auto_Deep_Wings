import cv2
import os

# change directory to parent directory of all folders
# This should/will be replaced with a command line argument
os. chdir("/home/stephen/Documents/deep_wings/dec_col")

# loop over all files in the parent directory, this will be changed to the
# command line argument
for directory in os.listdir("/home/stephen/Documents/deep_wings/dec_col"):
    # get the sample name by first grabbing the basename and then stripping the extension
    # this may need to be changed to account for other file types e.g. .png etc.
    sample_name = os.path.basename("/home/stephen/Documents/deep_wings/dec_col/{}.jpg".format(directory))
    sample_name = sample_name.rsplit( ".jpg", 1)[0]
    # print the sample name to screen to display progress
    print(sample_name)
    try:
        image = cv2.imread(r"/home/stephen/Documents/deep_wings/dec_col/{}/{}.jpg".format(directory, directory))
    except FileNotFoundError:
        print('''File does not exist or does not follow \n
              correct naming convention. \n
              Please ensure the image with the full slide \n
              is named the exact same as the folder which contains it.
              ''')
    original = image.copy()

    dimensions = image.shape

    # crop image to remove left hand side of slide which only contains the samples name
    x = 3000
    y = 0
    crop_img = image[y:dimensions[0], 800:dimensions[1]].copy()
    original_cropped = crop_img.copy()

    # grayscale, Gaussian blur, Otsu's threshold, dilate
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    dilate = cv2.dilate(thresh, kernel, iterations=1)

    # Find contours, obtain bounding box coordinates, and extract region of interest
    image_contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_contours = image_contours[0] if len(image_contours) == 2 else image_contours[1]
    image_number = 0
    for c in image_contours:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(crop_img, (x, y), (x + w, y + h), (36,255,12), 2)
        original_cropped_border = cv2.copyMakeBorder(original_cropped, 100, 100, 100, 100, cv2.BORDER_CONSTANT)
        ROI = original_cropped[y-20:y+h+25, x-5:x+w+50]
        # apply some padding to the border to catch wings which are too close for cropping to pick up?
        #ROI = cv2.copyMakeBorder(ROI, 100, 100, 100, 100, cv2.BORDER_CONSTANT)
        # write image to file, location of which should be changed to a command line argument
        cv2.imwrite("/home/stephen/Documents/deep_wings/dec_col/{}/{}_{}.png".format(sample_name,sample_name,image_number), ROI)
        image_number += 1


    # loop through all the images we just created and delete the small ones which
    # do not contain images of the wings
    # this will need to be recoded to contain the directory argument from user input
    for file in os.listdir("/home/stephen/Documents/deep_wings/dec_col/{}/".format(sample_name)):
        if file.endswith('.png'):
            if os.path.getsize("/home/stephen/Documents/deep_wings/dec_col/{}/{}".format(sample_name,file)) < 20000:
                os.remove("/home/stephen/Documents/deep_wings/dec_col/{}/{}".format(sample_name,file))


