import sys, os
from utils import load_dictionary
from multiprocessing import Pool

def find_oov(input_args):
    text, dictionary = input_args
    oov_dict = {}
    filename, content = text.strip().split('|', 1)
    for word in content.strip().split(' '):
        if word not in dictionary:
            oov_dict[word] = filename
    return oov_dict
if __name__=='__main__':
    input_text = sys.argv[1]
    dict_path  = sys.argv[2]
    
    dictionary = load_dictionary(dict_path, delimiter='\t')
    dict_name = os.path.splitext(os.path.basename(dict_path))[0]
    text_file_name = os.path.splitext(os.path.basename(input_text))[0]
    text_dir = os.path.dirname(input_text.rstrip('/'))
    
    out_text_file = os.path.join(text_dir, text_file_name + '_oovOf_' + dict_name)
    oov_dict = {}
    
    input_args = []
    with open(input_text) as f:
        for line in f:
            input_args.append([line.strip(), dictionary])
    with Pool(16) as p:
        results = p.map(find_oov, input_args)
    
    for sub_oov_dict in results:
        for oov, filename in sub_oov_dict.items():
            oov_dict[oov] = filename
    
    # oov_list = []
    # with open(input_text) as f:
    #     for line in f:
    #         # print(line)
    #         filename, content = line.strip().split('|', 1)
    #         for word in content.strip().split(' '):
    #             if word not in oov_list and word not in dictionary:
    #                 oov_list.append(word)
    
    with open(out_text_file, 'w')  as f:
        for line in oov_dict.keys():
            f.write(line + '\n')