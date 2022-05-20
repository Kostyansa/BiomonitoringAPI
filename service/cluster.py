import logging

from sklearn.cluster import DBSCAN
from ast import Num
import cv2
import numpy as np
from torch import ne
import entity.bioobject as bioobject
import utils.color as color


class ModelService:

    def __init__(self):
        pass

    def analyse(self, bioobject_entity: bioobject.Bioobject):
        image = cv2.imread(f'./picture/{bioobject_entity.name}')

        image = cv2.resize(image, (256, 112))
        image_original = image.copy()
        image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, image_thresh = cv2.threshold(image_grayscale, 245, 255, cv2.THRESH_BINARY)

        mask = []
        for i in range(112):
            for j in range(256):
                if image_thresh[i][j] == 0:
                    mask.append([i, j])

        area_of_object = len(mask)

        data_for_clustering = []
        min_distance = [1, 1, 1]
        max_distance = [0, 0, 0]
        test = [0, 0, 0]
        for coord in mask:
            i, j = coord
            tmp_array = [np.tanh(image_original[i][j][0] / 255),
                         np.tanh(image_original[i][j][1] / 255),
                         np.tanh(image_original[i][j][2] / 255)]
            data_for_clustering.append(tmp_array)
            tmp = tmp_array[0] + tmp_array[1] + tmp_array[2]
            if tmp < min_distance[0] + min_distance[1] + min_distance[2]:
                min_distance = tmp_array
            if tmp > max_distance[0] + max_distance[1] + max_distance[2]:
                max_distance = tmp_array
            test[0] += tmp_array[0]
            test[1] += tmp_array[1]
            test[2] += tmp_array[2]

        test[0] /= len(mask)
        test[1] /= len(mask)
        test[2] /= len(mask)
        kek = [0, 0, 0]

        epsilon_precision = np.linalg.norm(np.array(max_distance) - np.array(min_distance)) * 0.0078

        data_for_clustering = np.array(data_for_clustering)

        clustering = DBSCAN(eps=epsilon_precision, min_samples=2, n_jobs=-1).fit(data_for_clustering)

        labels_for_image = clustering.labels_
        labels_quantity_ = clustering.labels_.max() - clustering.labels_.min() + 2
        logging.debug(f'Labels: {labels_quantity_}')

        colors = color.color_randomizer(labels_quantity_)

        for k in range(len(labels_for_image)):
            i, j = mask[k]
            image[i][j][0] = colors[labels_for_image[k]][0]
            image[i][j][1] = colors[labels_for_image[k]][1]
            image[i][j][2] = colors[labels_for_image[k]][2]

        median_blur_image = cv2.medianBlur(image, 5)

        clusters = {}

        for coords in mask:
            i, j = coords
            hex_color = color.RGB2HEX(median_blur_image[i][j])
            if not (hex_color in clusters):
                clusters[hex_color] = {'area': 1,
                                       'median_original_color': [int(image_original[i][j][0]),
                                                                 int(image_original[i][j][1]),
                                                                 int(image_original[i][j][2])],
                                       'coords': [[i, j]]}
                # clusters.add(Cluster(median_blur_image[i][j], image_original[i][j]))
            else:
                clusters[hex_color]['area'] += 1
                clusters[hex_color]['median_original_color'][0] += image_original[i][j][0]
                clusters[hex_color]['median_original_color'][1] += image_original[i][j][1]
                clusters[hex_color]['median_original_color'][2] += image_original[i][j][2]
                clusters[hex_color]['coords'].append([i, j])

        for cluster in clusters:
            if (clusters[cluster]['area'] >= 10):
                clusters[cluster]['median_original_color'][0] /= clusters[cluster]['area']
                clusters[cluster]['median_original_color'][1] /= clusters[cluster]['area']
                clusters[cluster]['median_original_color'][2] /= clusters[cluster]['area']
                if (clusters[cluster]['median_original_color'][0] < clusters[cluster]['median_original_color'][2]
                        > clusters[cluster]['median_original_color'][1] and 15 <=
                        clusters[cluster]['median_original_color'][0] <= 84 and
                        36 <= clusters[cluster]['median_original_color'][1] <= 103 and 93 <=
                        clusters[cluster]['median_original_color'][2] <= 144):
                    clusters[cluster]['type'] = 'rot'

                elif (clusters[cluster]['median_original_color'][0] < clusters[cluster]['median_original_color'][1]
                      > clusters[cluster]['median_original_color'][2] and 66 <=
                      clusters[cluster]['median_original_color'][0] <= 146 and
                      66 <= clusters[cluster]['median_original_color'][1] <= 206 and 60 <=
                      clusters[cluster]['median_original_color'][2] <= 188):
                    clusters[cluster]['type'] = 'green_mould'

                elif (0.8 <= clusters[cluster]['median_original_color'][0] / clusters[cluster]['median_original_color'][
                    1] <= 1 and
                      0.8 <= clusters[cluster]['median_original_color'][1] / clusters[cluster]['median_original_color'][
                          2] <= 1 and
                      0.8 <= clusters[cluster]['median_original_color'][0] / clusters[cluster]['median_original_color'][
                          2] <= 1 and
                      clusters[cluster]['median_original_color'][0] < 150):
                    clusters[cluster]['type'] = 'necrosis'
                elif (0.8 <= clusters[cluster]['median_original_color'][0] / clusters[cluster]['median_original_color'][
                    1] <= 1 and
                      0.8 <= clusters[cluster]['median_original_color'][1] / clusters[cluster]['median_original_color'][
                          2] <= 1 and
                      0.8 <= clusters[cluster]['median_original_color'][0] / clusters[cluster]['median_original_color'][
                          2] <= 1 and
                      clusters[cluster]['median_original_color'][0] > 150):
                    clusters[cluster]['type'] = 'white_mold'
                else:
                    clusters[cluster]['type'] = 'normal'
            else:
                clusters[cluster] = None

        cv2.waitKey(0)
        tmp_data = {'necrosis_area' : 0, 'rot_area' : 0, \
            'white_mold_area' : 0, 'green_mold_area' : 0}
        for cluster in clusters:
            if clusters[cluster] == None:
                continue
            if (clusters[cluster]['type'] == 'normal'):
                for coord in clusters[cluster]['coords']:
                    i, j = coord
                    median_blur_image[i][j][0] = 0
                    median_blur_image[i][j][1] = 255
                    median_blur_image[i][j][2] = 0
            elif (clusters[cluster]['type'] == 'necrosis'):
                tmp_data['necrosis_area'] += clusters[cluster]['area']
                for coord in clusters[cluster]['coords']:
                    i, j = coord
                    median_blur_image[i][j][0] = 0
                    median_blur_image[i][j][1] = 0
                    median_blur_image[i][j][2] = 0
            elif (clusters[cluster]['type'] == 'white_mold'):
                tmp_data['white_mold_area'] += clusters[cluster]['area']
                for coord in clusters[cluster]['coords']:
                    i, j = coord
                    median_blur_image[i][j][0] = 255
                    median_blur_image[i][j][1] = 255
                    median_blur_image[i][j][2] = 0
            elif (clusters[cluster]['type'] == 'green_mold'):
                tmp_data['green_mold_area'] += clusters[cluster]['area']
                for coord in clusters[cluster]['coords']:
                    i, j = coord
                    median_blur_image[i][j][0] = 255
                    median_blur_image[i][j][1] = 0
                    median_blur_image[i][j][2] = 0
            elif (clusters[cluster]['type'] == 'rot'):
                tmp_data['rot_area'] += clusters[cluster]['area']
                for coord in clusters[cluster]['coords']:
                    i, j = coord
                    median_blur_image[i][j][0] = 0
                    median_blur_image[i][j][1] = 0
                    median_blur_image[i][j][2] = 255

        result_data = {'path_to_picture': f'/picture/{bioobject_entity.name}_median_blur_image.png', 
        'necrosis_percentage':   round((tmp_data['necrosis_area'] * 100) / area_of_object, 1),
        'rot_percentage':  round((tmp_data['rot_area'] * 100)  / area_of_object, 1), 
        'green_mold_percentage': round((tmp_data['green_mold_area'] * 100) / area_of_object, 1), 
        'white_mold_percentage':  round((tmp_data['white_mold_area'] * 100) / area_of_object, 1)}

        cv2.imwrite('.' + result_data['path_to_picture'], median_blur_image)
        return result_data
