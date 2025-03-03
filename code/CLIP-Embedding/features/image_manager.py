import matplotlib.pyplot as plt
from features.features import ImageEmbedding, Text
from features.process_images import ProcessImages
from similaritys.similarity import Similarity
from environment.environment import DistanteTextsRelevace as env
from environment.environment import ImageEmbeddingEnv as image_env
from environment.environment import Colab as colab
import os

if colab.use_in_local():
    unsimilates_texts = [Text(text) for text in env.get_texts()]

process = ProcessImages()
class ImageFeature:
    def __init__(self, image_path:str = None,name = None, data_path = None, delete_relevants = True) -> None:
        self.name = name
        self.path = image_path
        self.origin:ImageEmbedding = None
        self.images:list[ImageEmbedding] = []
        self.masks:list[ImageEmbedding] = []
        self.ranking:dict[ImageEmbedding:float] = {}
        if image_path is not None:
            self.set_images(image_path)
            # self.set_ranking()
            if delete_relevants:
                self.delete_relevant_images()
            self.set_neighbords()

    def set_ranking(self):
        result = {}
        for image in self.images:
            if image == self.origin: continue
            
            similarity = Similarity.cosine(image, self.origin)
            result[similarity] = image

        result = dict(sorted(result.items(),reverse=True))
        end= {value: key for key,value in zip(result.keys(), result.values())}
        self.ranking = end
        return self.ranking

    def get_rank(self, image:ImageEmbedding):
        try:
            return self.ranking[image]
        except:
            return None
        
    def from_list(self, list_images):
        self.images = []

        for feature in list_images['images']:
            image = ImageEmbedding(None, feature[1])    
            image.set_embedding(feature[0])
            image.set_id(self.__len__())
            self.images.append(image)
        
        for i, feature in zip(range(self.__len__()),list_images['images']):
            image = self.images[i]
            for key in image.neighbords.keys():
                for neigh in feature[2][key]: 
                    image.neighbords[key].append(self.convert_to_neighbord(neigh))
        
        self.path = list_images['path']
        self.name = self.path.split(os.path.sep)[-1]

    def clear(self):
        self.images = []

    def to_list(self):
        return {'images':[image.to_list() for image in self.images], 'path': self.path}
    
    def add_image(self, image:ImageEmbedding):
        image.set_id(self.__len__())
        self.images.append(image)
    
    def add_mask(self, image:ImageEmbedding):
        image.set_id(self.masks.__len__())
        image.name = 'mask'
        self.masks.append(image)
  
    def set_images(self, path):
        # images = process.get_images(path)
        segmentations = process.get_segmentations(path)
        images = segmentations[image_env.KEY_IMAGES]
        masks = segmentations['mask']
        
        self.origin = ImageEmbedding(process.load_cv2_image(path),None)
        self.images = [self.origin]
        for image in images:
            self.add_image(image)
        
        self.masks = [self.origin]
        for mask in masks:
            self.add_mask(mask)
            
    def get_image_from_id(self, id):
        return self.images[id]
    
    def convert_to_neighbord(self, neigh):
        return (self.get_image_from_id(neigh[0]), neigh[1])
    
    def __len__(self):
        return len(self.images)
    
    def set_neighbords(self):
        segms = [image for image in self.images if image != self.images[0]]#No usar la imagen original
        for image in segms:
                image.set_neighbords(segms)

    def __getitem__(self, index)-> ImageEmbedding:
       return self.images[index]
    
    def plot_regions(self):
        fig, ax = plt.subplots()
        ax.invert_yaxis()
        # Mostrar la imagen en los ejes con origin='lower'
        if self.images[0].image is not None:
            ax.imshow(self.images[0].image, extent=[0, 1, 1, 0], alpha=0.5)
        
        for image in self.images:
            if image == self.images[0]:continue #la primera imagen es la original
            image.plot_region(ax)
        plt.show()

    def plot_from_index(self, index):
        fig, ax = plt.subplots()
        ax.invert_yaxis()
        if self.images[0].image is not None:
            ax.imshow(self.images[0].image, extent=[0, 1, 1, 0], alpha=0.5)

        image = self[index]
        image.plot_region(ax)
        plt.title(f'{image}   pos: {image.position}')
        plt.show()

    def plot_from_image(self, image:ImageEmbedding):
        fig, ax = plt.subplots()
        ax.invert_yaxis()
        if self.images[0].image is not None:
            ax.imshow(self.images[0].image, extent=[0, 1, 1, 0], alpha=0.5)

        image.plot_region(ax)
        plt.title(f'{image}   pos: {image.position}')
        plt.show()

    def delete_relevant_images(self, print_ = False, value = None, percentaje = None):
        def is_image_relevant_for_all(image, value, percentaje):
            count_relevance = 0
            for text in unsimilates_texts:
                if value is None:
                    value = env.umbral
                if Similarity.cosine(text, image) > value:
                    count_relevance +=1
            if print_:
                print(f'{image}: {count_relevance/len(unsimilates_texts)}')
            if percentaje is None:
                percentaje = env.percentaje
            return count_relevance/len(unsimilates_texts) > percentaje
        
        images = [image for image in self.images if image != self.origin]
        for image in images:
            if is_image_relevant_for_all(image, value=value, percentaje=percentaje):
                self.images.remove(image)
        
        # self.set_neighbords()        
