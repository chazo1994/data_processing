import sys
import os
import glob
import argparse
import json
from scipy.io.wavfile import read, write
import unicodedata

from clean_text import clean_text, remove_punc

NORM_REPLACE_PATTERNS = {
    'cv': 'xi vi',
    'sơmi': 'sơ mi',
    'haizzz': 'haizz',
    'Haizzz': 'haizz',
    'hotsearch': 'hot search',
    'gl': 'gi eo',
    'Sadako': 'sa đa cô',
    'sadako': 'sa đa cô'
}

def simple_norm_text(text):
    words = []
    for word in text.split():
        word = unicodedata.normalize('NFC', word)
        if word:
            words.append(word)
    return ' '.join(words)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', type=str,
                        help='Wave directory', required=True)
    parser.add_argument('-o', '--outdir', type=str,
                        help='Output data directory', required=True)
    parser.add_argument('-s', '--speaker', type=str,
                        help='speaker name', required=True)
    # parser.add_argument('-sp', '--split_audio', action='store_true',
    #                     help='Split original audio to segments')
    args = parser.parse_args()
    input_data_dir = args.input_dir
    output_data_dir = args.outdir
    speaker = args.speaker
    os.makedirs(output_data_dir, exist_ok=True)
    outwav_dir = os.path.join(output_data_dir, 'wavs')
    os.makedirs(outwav_dir, exist_ok=True)
    wavfiles = glob.glob(os.path.join(input_data_dir, '*.wav'))
    metadata = {'audios': {}}
    text_remove_punc = []
    total_duration = 0
    total_samples = 0
    for wavfile in wavfiles:
        filename = os.path.splitext(os.path.basename(wavfile))[0]
        label_file = os.path.join(input_data_dir, filename + '.txt')
        sampling_rate, data = read(wavfile)
        #Get channel 0
        if len(data.shape) > 1:
            data = data[:,0]
        if os.path.isfile(label_file):
            print('Process: {}'.format(label_file))
            with open(label_file, encoding='utf-8') as f:
                sentence_idx = 0
                paragraph_id = 0
                for line in f:
                    print('sen idx: {}, line: {}'.format(sentence_idx, line))
                    start, end, content = line.strip().split('\t')
                    if content.strip() == '<end_chapter>':
                        sentence_idx = 0
                        paragraph_id += 1
                        continue

                    start = float(start)
                    end = float(end)
                    start_pos = int(start*sampling_rate)
                    end_pos = int(end*sampling_rate)
                    
                    original_audio_id = filename
                    
                    raw_script=content
                    script = simple_norm_text(clean_text(raw_script.lower(), custom_replace_patterns=NORM_REPLACE_PATTERNS))
                    global_sample_id = original_audio_id + '-' + str(paragraph_id) + '-' + str(sentence_idx)
                    text_remove_punc.append([global_sample_id, remove_punc(script)])
                    # if args.split_audio:
                    audio_segment = data[start_pos:end_pos]
                    audio_path = os.path.join(outwav_dir, global_sample_id + '.wav')
                    write(audio_path, sampling_rate, audio_segment)
                    
                    metadata['audios'][global_sample_id] = {
                        "position": sentence_idx,
                        "start_idx": start,
                        "end_idx": end,
                        "raw_script": raw_script,
                        "script": script,
                        "paragraph_id": paragraph_id,
                        "speaker_id": speaker,
                        "original_audio_id": original_audio_id
                    }
                    total_duration += end-start
                    total_samples += 1
                    sentence_idx += 1
    
    # Write metadata
    metadata['total_duration'] = total_duration / 3600
    metadata['total_samples'] = total_samples
    metadata_file = os.path.join(output_data_dir, 'metadata.json')
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
    
    #Write raw script
    raw_script_file = os.path.join(output_data_dir, 'raw_text.txt')
    with open(raw_script_file, 'w', encoding='utf-8') as f:
        for sample_id, sample_data in metadata['audios'].items():
            line = sample_id + '|' + sample_data['raw_script']
            f.write(line + '\n')
    
    #Write clean script
    script_file = os.path.join(output_data_dir, 'clean_text.txt')
    with open(script_file, 'w', encoding='utf-8') as f:
        for sample_id, sample_data in metadata['audios'].items():
            line = sample_id + '|' + sample_data['script']
            f.write(line + '\n')
    #Write clean no punc script
    script_file = os.path.join(output_data_dir, 'clean_text.remove_punc.txt')
    with open(script_file, 'w', encoding='utf-8') as f:
        for sample_id, text in text_remove_punc:
            line = sample_id + '|' + text
            f.write(line + '\n')
