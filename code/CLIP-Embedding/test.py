from features.features import ImageEmbedding
from features.image_manager import ImageFeature
from retrieval_system.data import ImagesDataset 

image_0 = ImageEmbedding(None, (0.2,0.1))
image_0.set_limits((0.1,0.3,0,0.2))
image_1 = ImageEmbedding(None, (0.5,0.2))
image_1.set_limits((0.4,0.6,0.1,0.3))
image_2 = ImageEmbedding(None, (0.4,0.5))
image_2.set_limits((0.2,0.6,0.4,0.6))
image_3 = ImageEmbedding(None, (0.8,0.4))
image_3.set_limits((0.7,0.9,0.2,0.6))

image_4 = ImageEmbedding(None, (0.55,0.8))
image_4.set_limits((0.2,0.9,0.7,0.9))
# image_4.set_limits((0.2,0.9,0.7,0.9))


images = ImageFeature()
images.add_image(ImageEmbedding(None,None))
images.add_image(image_0)
images.add_image(image_1)
images.add_image(image_2)
images.add_image(image_3)
images.add_image(image_4)

images.set_neighbords()
images.path = '/1/2/3/4/image1.jpg'

data = ImagesDataset()
data.append_image_set(images)
data.save_to_path()
data = ImagesDataset()
data.load_from_dataset_path()

# temp = images.to_list()
# new_images = ImageFeature()
# new_images.from_list(temp)

# for image, new_images in zip(images, new_images.images):
for image in images:
    # print(image.info())
    print(image)
    # image.print_neighbords()
    for neigh in image.neighbords:
        print (f'{neigh}: {image.neighbords[neigh]}')
    print('------------------------------------------')
images.plot_regions()
