import sys
import os
import glob
from scipy.io.wavfile import read, write
if __name__=='__main__':
    input_data_dir = sys.argv[1]
    output_data_dir = sys.argv[2]
    os.makedirs(output_data_dir, exist_ok=True)
    wavfiles = glob.glob(os.path.join(input_data_dir, '*.wav'))
    
    for wavfile in wavfiles:
        filename = os.path.splitext(os.path.basename(wavfile))[0]
        label_file = os.path.join(input_data_dir, filename + '.wav')
        sampling_rate, data = read(wavfile)
        #Get channel 0
        if len(data.shape) > 1:
            data = data[:,0]
        if os.path.isfile(label_file):
            with open(label_file) as f:
                sentence_idx = 0
                for line in f:
                    start, end, content = line.strip().split('\t')
                    start_pos = int(start*sampling_rate)
                    end_pos = int(end*sampling_rate)
                    audio_segment = data[0][start_pos:end_pos]
                    
                    sentence_idx += 1
