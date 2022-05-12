from sklearn.cluster import DBSCAN
import cv2
import numpy as np
import entity.bioobject as bioobject
import utils.color as color


class ModelService:

    def __init__(self):
        pass

    def analyse(self, bioobject_entity: bioobject.Bioobject):
        image = bioobject_entity.img()

        image = cv2.resize(image, (256, 112))
        image_original = image.copy()
        image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, image_thresh = cv2.threshold(image_grayscale, 254, 255, cv2.THRESH_BINARY)

        mask = []
        for i in range(112):
            for j in range(256):
                if image_thresh[i][j] == 0:
                    mask.append([i, j])

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
        test_precision = np.linalg.norm(np.array(kek) - np.array(test)) * 0.0152

        epsilon_precision = np.linalg.norm(np.array(max_distance) - np.array(min_distance)) * 0.0078

        data_for_clustering = np.array(data_for_clustering)

        clustering = DBSCAN(eps=epsilon_precision, min_samples=2, n_jobs=-1).fit(data_for_clustering)

        labels_for_image = clustering.labels_
        labels_quantity_ = clustering.labels_.max() - clustering.labels_.min() + 2
        print(labels_quantity_)

        colors = color.color_randomizer(labels_quantity_)

        for k in range(len(labels_for_image)):
            i, j = mask[k]
            image[i][j][0] = colors[labels_for_image[k]][0]
            image[i][j][1] = colors[labels_for_image[k]][1]
            image[i][j][2] = colors[labels_for_image[k]][2]

        cv2.imwrite('image_clustered.png', image)

        median_blur_image = cv2.medianBlur(image, 5)
        cv2.imwrite('median_blur_image.png', median_blur_image)

        clusters = {}

        for coords in mask:
            i, j = coords
            hex_color = color.RGB2HEX(median_blur_image[i][j])
            if not (hex_color in clusters):
                clusters[hex_color] = {'area': 1, 'median_original_color': [int(image_original[i][j][0]),
                                                                            int(image_original[i][j][1]),
                                                                            int(image_original[i][j][2])]}
                # clusters.add(Cluster(median_blur_image[i][j], image_original[i][j]))
            else:
                clusters[hex_color]['area'] += 1
                clusters[hex_color]['median_original_color'][0] += image_original[i][j][0]
                clusters[hex_color]['median_original_color'][1] += image_original[i][j][1]
                clusters[hex_color]['median_original_color'][2] += image_original[i][j][2]

        for cluster in clusters:
            if (clusters[cluster]['area'] >= 10):
                clusters[cluster]['median_original_color'][0] /= clusters[cluster]['area']
                clusters[cluster]['median_original_color'][1] /= clusters[cluster]['area']
                clusters[cluster]['median_original_color'][2] /= clusters[cluster]['area']
            else:
                clusters[cluster] = None

        cv2.waitKey(0)
        print(1)
