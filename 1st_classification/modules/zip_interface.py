# Copyright 2023 Ar-Ray-code
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2, glob, os, shutil, zipfile
from modules.image2txt import Image2Text

image2text = Image2Text('./cache/')
image2text.load_model()

class ZipInterface:
    def __init__(self):
        print("ZipInterface init")
        self.zip_extract_path = "./cache/zip_extract"
        self.zip_file_path = "./cache/upload.zip"
        os.makedirs('./cache/result/true', exist_ok=True)
        os.makedirs('./cache/result/false', exist_ok=True)
        print("Load transformer model done")

    def load(self,
             upload_zip_binary: bytes,
             prompt_text: str="a photography of",
             zip_extract_path: str="./cache/zip_extract",
             target_keywords: list=["person", "human", "man", "woman", "child", "children", "people"]):

        self.prompt_text = prompt_text
        self.zip_extract_path = zip_extract_path
        self.target_keywords = target_keywords

        print("prompt_text: ", self.prompt_text)
        print("zip_extract_path: ", self.zip_extract_path)
        print("target_keywords: ", self.target_keywords)

        self.true_list = {}
        self.false_list = {}

        # download and extract zip file
        with open(self.zip_file_path, mode='wb') as f:
            f.write(upload_zip_binary)
        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(self.zip_extract_path)

        self.images = []
        format_list = ["jpg", "jpeg", "png", "bmp", "tiff", "tif", "pgm", "ppm", "hdr", "webp"]
        format_list_upper = [format.upper() for format in format_list]
        format_list += format_list_upper

        for format in format_list:
            self.images += glob.glob(self.zip_extract_path + "/**/*." + format, recursive=True)
        self.images.sort()
        print(self.images)

    def save(self, save_path: str="./results.txt"):
        with open(save_path, mode='w') as f:
            f.write('\n'.join(self.results))

    def divide_zip(self) -> str:
        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            for image_path in self.true_list.keys():
                image = zip_ref.read(os.path.basename(image_path))
                with open("./cache/result/true/" + os.path.basename(image_path), mode='wb') as f:
                    f.write(image)
            for image_path in self.false_list.keys():
                image = zip_ref.read(os.path.basename(image_path))
                with open("./cache/result/false/" + os.path.basename(image_path), mode='wb') as f:
                    f.write(image)

        with zipfile.ZipFile('./cache/result.zip', 'w') as zip_ref:
            for root, _, files in os.walk('./cache/result'):
                for file in files:
                    zip_ref.write(os.path.join(root, file), arcname=os.path.join(root.replace('./cache/result/', ''), file))
        return os.path.abspath('./cache/result.zip')

    def cleanup(self):
        if os.path.exists('./cache/result.zip'):
            shutil.rmtree('./cache/result/')
            shutil.rmtree('./cache/zip_extract/')
        os.makedirs('./cache/result/true', exist_ok=True)
        os.makedirs('./cache/result/false', exist_ok=True)

    def run(self) -> str:
        global image2text
        self.results = []
        for image in self.images:
            image_raw = cv2.imread(image)
            text = image2text.convert(image_raw, self.prompt_text)
            if any(keyword in text for keyword in self.target_keywords):
                self.true_list[image] = text
            else:
                self.false_list[image] = text
            print('text: ', text)
            self.results.append(text)

        self.save()
        result_filename = self.divide_zip()
        self.cleanup()
        return result_filename

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('zip', type=str, help='zip file path')
    parser.add_argument('--prompt', type=str, default="a photography of", help='prompt text')

    args = parser.parse_args()
    zip_interface = ZipInterface()
    binary = None
    with open(args.zip, mode='rb') as f:
        binary = f.read()
        zip_interface.load(binary, args.prompt)
        result_filename = zip_interface.run()
        print("output: ", result_filename)
