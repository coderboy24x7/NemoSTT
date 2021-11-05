import os, copy, torch, json
from jiwer import wer
import nemo.collections.asr as nemo_asr
import pytorch_lightning as pl
cont = 0
metadata = open('/home/csanta/lili-asr/dataset/dev_trans.json')
quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="stt_es_quartznet15x5")
total_lines = len(metadata.read())
for line in metadata:
        json_load = json.loads(line)
        filename = json_load['audio_filepath'].split('/')[-1]
        text = json_load['text']
        inference = quartznet.transcribe(paths2audio_files=[os.path.join('/home/csanta/lili-asr/dataset/test/', filename)])
        error = wer(text, inference)
        cont = cont + error

print('Final WER:', cont/total_lines)