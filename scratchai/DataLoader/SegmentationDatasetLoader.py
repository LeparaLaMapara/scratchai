import numpy as np
import os
from ImageDatasetLoader import ImageDatasetLoader
from color_code import *
from PIL import Image

class SegmentationDatasetLoader(ImageDatasetLoader):

    def __init__(self, input_path, label_path, dataset_is=None, color_map=None):
        '''
        Constructor for the Segmentation Dataset Loader

        Arguemnts:
        - input_path : 
        - label_path : 
        - dataset_is : name of the dataset, if it is known then the color map will
                       be loaded by default, without the need of passing
                       Supported Datasets:
                       - CamVid : pass 'camvid' as value to this argument

        - color_map - dict - a dictionary where the key is the class name
                             and the value is a tuple or list with 3 elements
                             one for each channel. So each key is a RGB value.
        '''

        super().__init__(input_path, label_path)
            
        if str(dataset_is) == CAMVID:
            color_map = camvid_color_map
        
        self.dataset_is = dataset_is
        self.color_map = color_map
        self.classes = list(self.color_map.keys())
        self.colors = list(self.color_map.values())
        self.num_classes = len(color_map)

        # Check for unusualities in the given directory
        self.check()
    
    def check(self):
        if self.dataset_is is None and self.color_map is None:
            raise RuntimeError('Both \'dataset_is\' and \'color_map\' can\'t be None')
        super(SegmentationDatasetLoader, self).check()
        

    def create_masks(self, image=None, path=None):
        '''
        A class that creates masks for each of the classes

        Arguments:
        - Image.PIL - Semantic Segmented Image where each pixel is colored
                      with a specific color
                      The Image is of size H x W x C
                      where H is the height of the image
                            W is the width of the image
                            C is the number of channels (3)

        Returns:
        - np.ndarray - of size N x H x W
                       where N is the number of classes
                             H is the height of the image
                             W is the width of the image
        '''
        
        if image is None and path is None:
            raise RuntimeError('Either image or path needs to be passed!')

        if not path is None:
            if not os.path.exists(path):
                raise RuntimeError('You need to pass a valid path!\n \
                                    Try passing a number if you are having trouble reaching \
                                    the filename')
            image = np.array(Image.open(path)).astype(np.uint8)

        if image.shape[-1] > 3 or image.shape[-1] < 3:
            raise RuntimeError('The image passed has more than expected channels!')
        
        masks = []
        for ii in self.color_map:
            color_img = []
            for j in range(3):
                color_img.append(np.ones((img.shape[:-1])) * ii[j])
            img2 = np.array(color_img, dtype=np.uint8).transpose(1, 2, 0)
            masks.append(np.uint8((image == img2).sum(axis=-1) == 3))

        return np.array(masks)


    def decode_segmap(self, image=None, path=None, image_num=None):
        '''
        The method helps one get a colorful image where each color corresponds to each class

        Arguments:
        - Image - np.array - A 2D Image where each pixel position is a number indicating
                             the class to which is belongs
        
        Returns:
        - np.array - H x W x C
                    where each pixel position [x, y, :]
                    is a color representing its RGB color which is passed in
                    with the color_map while initializing this class
        '''

        if image is None and path is None:
            raise RuntimeError('Either image or path needs to be passed!')

        if not path is None:
            if not os.path.exists(path):
                raise RuntimeError('You need to pass a valid path!\n \
                                    Try passing a number if you are having trouble reaching \
                                    the filename')
            image = Image.open(path)

        r = np.zeros_like(image).astype(np.uint8)
        g = np.zeros_like(image).astype(np.uint8)
        b = np.zeros_like(image).astype(np.uint8)

        for label in range(0, self.num_classes):
            r[image == label] = self.colors[label][0]
            g[image == label] = self.colors[label][1]
            b[image == label] = self.colors[label][2]

        rgb = np.stack([r, g, b], axis=2)
        return rgb