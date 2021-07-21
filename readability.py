import re
import argparse

def ari(metrics):
    return 4.71 * metrics['Characters'] / metrics['Words'] + 0.5 * metrics['Words'] / metrics['Sentences'] - 21.43

def fk(metrics):
    return 0.39 * metrics['Words'] / metrics['Sentences'] + 11.8 * metrics['Syllables'] / metrics['Words'] - 15.59

def smog(metrics):
    return 1.043 * ((metrics['Polysyllables'] * 30 / metrics['Sentences']) ** 0.5) + 3.1291

def cl(metrics):
    return 5.88 * metrics['Characters'] / metrics['Words'] - 29.6 * metrics['Sentences'] / metrics['Words'] - 15.8

def pb(metrics):
    percents = metrics['Difficult words'] / metrics['Words'] * 100  # percents if difficult words
    return 0.1579 * percents + 0.0496 * metrics['Words'] / metrics['Sentences'] + (0 if percents < 5 else 3.6365)

formulas = {'ARI': ['Automated Readability Index', ari],
           'FK': ['Flesch–Kincaid readability tests', fk],
           'SMOG': ['Simple Measure of Gobbledygook', smog],
           'CL': ['Coleman–Liau index', cl],
           'PB': ['Probability-based score', pb]}

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--infile")
parser.add_argument("-w", "--words")
args = parser.parse_args()
file = open(args.infile)
text = '\n' + file.read()
file.close()
file = open(args.words)
no_difficult = file.read().split()
file.close()

metrics = {}
words = re.findall(r"\b[-\w,\\.]+\b", text)
metrics['The text is'] = text
metrics['Words'] = len(words)
metrics['Difficult words'] = 0
metrics['Sentences'] = len(re.findall(r'[.!?]+', text + '.'))
metrics['Characters'] = len(re.findall(r'[^\s)(]', text))
metrics['Syllables'] = 0
metrics['Polysyllables'] = 0
for word in words:
    word = word.lower()
    word_syllables = len(re.findall('[aeiouy]', word))  # vowels
    for pattern in [r'\w+e$', r'\w*[aeiouy]{2,3}\w*', r'\w*shed$', r'\w*des$', r'\w*ion[s]?$']:
        word_syllables -= (1 if re.match(pattern, word) else 0)
    metrics['Syllables'] += word_syllables if word_syllables > 0 else 1
    metrics['Polysyllables'] += 1 if word_syllables > 2 else 0
    metrics['Difficult words'] += 1 if word not in no_difficult else 0
for key in metrics.keys():
    print(f'{key}: {metrics[key]}')

inp = input("Enter the score you want to calculate (ARI, FK, SMOG, CL, PB, all): ")
methods = [inp] if inp != 'all' else ['ARI', 'FK', 'SMOG', 'CL', 'PB']

print()
year_old_summ = 0
for method in methods:
    score = formulas[method][1](metrics)
    if method != 'PB':
        year_old = [6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 24][int(score) - 1] if score < 14 else 25
    else:
        year_old = [10, 10, 10, 10, 10, 12, 14, 16, 18, 24][int(score)]
    print(f'{formulas[method][0]}: {score:.2f} (about {year_old}-year-olds)')
    year_old_summ += year_old

print(f'\nThis text should be understood in average by {(year_old_summ / len(methods)):.1f}-year-olds.')
