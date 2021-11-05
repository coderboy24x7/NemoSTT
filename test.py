import os, copy, torch, json
from jiwer import wer
import nemo.collections.asr as nemo_asr
import pytorch_lightning as pl
metadata = open('/home/csanta/lili-asr/dataset/jsons/dev_trans.json')
quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="stt_es_quartznet15x5")
for line in metadata:
        print(json.loads(line))
                        # print(quartznet.transcribe(paths2audio_files=[os.path.join(root, file)]))
