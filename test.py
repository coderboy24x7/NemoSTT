import os, copy, torch
import nemo.collections.asr as nemo_asr
import pytorch_lightning as pl
for root, dirs, files in os.walk("/home/csanta/lili-asr/dataset/test/"):
        for file in files:
                if file.endswith('.wav'):
                        quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="stt_es_quartznet15x5")
                        print(quartznet.transcribe(paths2audio_files=os.path.join(root, file)))
