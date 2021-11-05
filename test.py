import os
from nemo.collections.asr.models import ASRModel

# Iterate for each dict object in os.walk()
for root, dirs, files in os.walk("/home/csanta/lili-asr/dataset/test/"):
        print(type(files))
        # asr_model = ASRModel.from_pretrained(model_name=cfg.pretrained_name, map_location=device)  # type: ASRModel
        # model_name = cfg.pretrained_name