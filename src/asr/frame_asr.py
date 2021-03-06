import numpy as np
from src.asr.audio_data_layer import AudioDataLayer
from torch.utils.data import DataLoader
import copy, torch



# inference method for audio signal (single instance)

class FrameASR:
    def __init__(self, model_definition,
                 frame_len=2, frame_overlap=2.5,
                 offset=10, asr_model=None, cfg=None):
        '''
        Args:
          frame_len: frame's duration, seconds
          frame_overlap: duration of overlaps before and after current frame, seconds
          offset: number of symbols to drop for smooth streaming
        '''
        self.vocab = list(model_definition['labels'])
        self.vocab.append('_')

        self.sr = model_definition['sample_rate']
        self.frame_len = frame_len
        self.n_frame_len = int(frame_len * self.sr)
        self.frame_overlap = frame_overlap
        self.n_frame_overlap = int(frame_overlap * self.sr)
        timestep_duration = model_definition['AudioToMelSpectrogramPreprocessor']['window_stride']
        for block in model_definition['JasperEncoder']['jasper']:
            timestep_duration *= block['stride'][0] ** block['repeat']
        self.n_timesteps_overlap = int(frame_overlap / timestep_duration) - 2
        self.buffer = np.zeros(shape=2 * self.n_frame_overlap + self.n_frame_len,
                               dtype=np.float32)
        self.offset = offset
        self.reset()
        self.asr_model = asr_model
        self.cfg = cfg
        self.data_layer = AudioDataLayer(sample_rate=self.cfg.preprocessor.sample_rate)
        self.data_loader = DataLoader(self.data_layer, batch_size=1, collate_fn=self.data_layer.collate_fn)

    def infer_signal(self, model, signal):
        self.data_layer.set_signal(signal)
        batch = next(iter(self.data_loader))
        audio_signal, audio_signal_len = batch
        audio_signal, audio_signal_len = audio_signal.to(self.asr_model.device), audio_signal_len.to(self.asr_model.device)
        log_probs, encoded_len, predictions = model.forward(
            input_signal=audio_signal, input_signal_length=audio_signal_len
        )
        return log_probs

    def _decode(self, frame, offset=0):
        assert len(frame) == self.n_frame_len
        self.buffer[:-self.n_frame_len] = self.buffer[self.n_frame_len:]
        self.buffer[-self.n_frame_len:] = frame
        logits = self.infer_signal(self.asr_model, self.buffer).cpu().numpy()[0]
        # print(logits.shape)
        decoded = self._greedy_decoder(
            logits[self.n_timesteps_overlap:-self.n_timesteps_overlap],
            self.vocab
        )
        return decoded[:len(decoded) - offset]

    @torch.no_grad()
    def transcribe(self, frame=None, merge=True):
        if frame is None:
            frame = np.zeros(shape=self.n_frame_len, dtype=np.float32)
        if len(frame) < self.n_frame_len:
            frame = np.pad(frame, [0, self.n_frame_len - len(frame)], 'constant')
        unmerged = self._decode(frame, self.offset)
        if not merge:
            return unmerged
        return self.greedy_merge(unmerged)

    def reset(self):
        '''
        Reset frame_history and decoder's state
        '''
        self.buffer = np.zeros(shape=self.buffer.shape, dtype=np.float32)
        self.prev_char = ''

    @staticmethod
    def _greedy_decoder(logits, vocab):
        s = ''
        for i in range(logits.shape[0]):
            s += vocab[np.argmax(logits[i])]
        return s

    def greedy_merge(self, s):
        s_merged = ''

        for i in range(len(s)):
            if s[i] != self.prev_char:
                self.prev_char = s[i]
                if self.prev_char != '_':
                    s_merged += self.prev_char
        return s_merged