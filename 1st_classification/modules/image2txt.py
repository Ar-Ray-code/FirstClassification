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

import numpy as np
import os
import torch

from transformers import BlipProcessor, BlipForConditionalGeneration

class Image2Text:
    def __init__(self, cache_dir: str='./cache/'):
        self.cache_dir = cache_dir
    def load_model(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-large",
            torch_dtype=torch.float16,
            cache_dir=self.cache_dir).to("cuda")
        os.makedirs(self.cache_dir, exist_ok=True)

    def convert(self, image: np.ndarray, text: str="a photography of") -> str:
        print("image shape: ", image.shape)
        print("text: ", text)
        inputs = self.processor(image, text, return_tensors="pt").to("cuda", torch.float16)
        out = self.model.generate(**inputs)
        text = self.processor.decode(out[0], skip_special_tokens=True)
        return text
