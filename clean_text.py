import sys, os
REPLACE_PATTERNS = {
        ',': ' , ',
        '<': ' ',
        '.': ' . ',
        '…': ' . ',
        '...': ' . ',
        '……': ' . ',
        '"...': ' . ',
        '...?': ' . ',
        '>': ' ',
        '/': ' ',
        '?': ' ? ',
        ':': ' : ',
        ';': ' ; ',
        '"': ' ',
        '“': ' ',
        '”': ' ',
        '[': ' ',
        ']': ' ',
        '{': ' ',
        '}': ' ',
        '|': ' ',
        '~': ' ',
        '`': ' ',
        '!': ' ! ',
        '@': ' ',
        '#': ' ',
        '$': ' ',
        '%': ' ',
        '^': ' ',
        '&': ' ',
        '*': ' ',
        '(': ' ',
        ')': ' ',
        '_': ' ',
        '–': ' ',
        '-': ' ',
        '+': ' ',
        '=': ' ',
        ' \'': ' ',
        '\' ': ' ',
        '--': ' ',
        '---': ' ',
        '___': ' ',
        '—': ' ',
        '**': ' ',
        'no-sir-ee': 'no sir ee',
        '18': 'eighteen',
        '1908': 'nineteen oh eight',
        '16': 'sixteen'
    }
EXCLUDE_PATTERNS = [
    "mr.",
    "ms.",
    "dr."
]
def clean_text(text):
    text = ' ' + text + ' ' #Trick to remove '\'' at the begin and the end of sentence
    for exclude_pattern in EXCLUDE_PATTERNS:
        #TODO
        pass
    
    for k, v in REPLACE_PATTERNS.items():
        text = text.replace(k, v)
    while True:
        tmp = text.replace('  ', ' ')
        if tmp == text:
            break
        else:
            text = tmp
    return text.strip()
if __name__=='__main__':
    input_text = sys.argv[1]
    output_text = sys.argv[2]
    delimiter = "|"
    
    
    text_list = []
    with open(input_text) as f:
        for line in f:
            print(line)
            filename, content = line.strip().split(delimiter, 1)
            content = clean_text(content)
            # content = ' ' + content + ' ' #Trick to remove '\'' at the begin and the end of sentence
            # for exclude_pattern in exclude_patterns:
            #     #TODO
            #     pass
            
            # for k, v in replace_patterns.items():
            #     content = content.replace(k, v)
            # while True:
            #     tmp = content.replace('  ', ' ')
            #     if tmp == content:
            #         break
            #     else:
            #         content = tmp
            
            text_list.append(filename + delimiter + content.strip().lower())
    with open(output_text, 'w')  as f:
        for line in text_list:
            f.write(line + '\n')