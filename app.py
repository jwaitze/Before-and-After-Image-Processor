from PIL import Image
import os, sys

def GetFilesListFromDirectory(path):
    file_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return file_list

image_path = os.getcwd() + '\\raw\\'
done_path = os.getcwd() + '\\processed\\'
if __name__ == '__main__':
    files = GetFilesListFromDirectory(image_path)

    max_number = 0
    for file in files:
        number = file[:file.index('.')]
        if number.isdigit() and int(number) > max_number:
            max_number = int(number)

    for i in range(1, max_number, 2):
        before = Image.open(image_path + str(i) + '.jpg')
        after = Image.open(image_path + str(i+1) + '.jpg')
        template = Image.open(image_path + 'template.jpg')

        aspect_ratio_before = 340 / before.size[0]
        aspect_ratio_after = 340 / after.size[0]

        before_width = aspect_ratio_before * before.size[0]
        before_height = aspect_ratio_before * before.size[1]
        before.thumbnail((before_width, before_height))

        after_width = aspect_ratio_after * after.size[0]
        after_height = aspect_ratio_after * after.size[1]
        after.thumbnail((after_width, after_height))

        template_height = before_height if before_height > after_height else after_height
        template_box = (0, template.size[0] - (54 + template_height), template.size[1], template.size[0])
        template_region = template.crop(template_box)
        
        template_region.paste(before, (0,0))
        template_region.paste(after, (360,0))

        template_region.save(done_path + str(int(((i-1)/2)+1)) + '.jpg')
        
    print('Completed. %i images processed.' % max_number)        
