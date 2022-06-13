from PIL import Image, ImageTk  # Image for open, ImageTk for display
from os.path import exists
import cv2
import numpy as np


class Steganography(object):

    @staticmethod
    def to_bin(data):
        """Convert `data` to binary format as string"""
        if isinstance(data, str):
            return ''.join([format(ord(i), "08b") for i in data])
        elif isinstance(data, bytes) or isinstance(data, np.ndarray):
            return [format(i, "08b") for i in data]
        elif isinstance(data, int) or isinstance(data, np.uint8):
            return format(data, "08b")
        else:
            raise TypeError("Type not supported.")

    @staticmethod
    def encode(imagePath, text):
        # read the image
        image = cv2.imread(imagePath)
        # maximum bytes to encode
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8
        if len(text) > n_bytes:
            raise ValueError(
                "[!] Insufficient bytes, need bigger image or less data.")
        text += "====="
        data_index = 0
        binary_secret_data = Steganography.to_bin(text)
        data_len = len(binary_secret_data)
        for row in image:
            for pixel in row:
                r, g, b = Steganography.to_bin(pixel)
                if data_index < data_len:
                    pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                    data_index += 1
                if data_index >= data_len:
                    break
        newImgFilePath = Steganography.fileExistance(
            Steganography.encodedName(imagePath))
        cv2.imwrite(newImgFilePath, image)
        return newImgFilePath

    @staticmethod
    def decode(imagePath):
        image = cv2.imread(imagePath)
        binary_data = ""

        for row in image:
            for pixel in row:
                r, g, b = Steganography.to_bin(pixel)
                binary_data += r[-1]
                binary_data += g[-1]
                binary_data += b[-1]
        all_bytes = [binary_data[i: i+8]
                     for i in range(0, len(binary_data), 8)]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "=====":
                break
        return decoded_data[:-5]

    def fileExistance(filePath):
        while exists(filePath):
            lastDot = filePath.rindex(".")
            fileName = filePath[0:lastDot]
            extension = filePath[lastDot+1:]

            filePath = fileName + "_copy." + extension
        return filePath

    def encodedName(filePath):
        lastDot = filePath.rindex(".")
        fileName = filePath[0:lastDot]
        extension = filePath[lastDot+1:]
        return fileName + "_encoded." + extension
