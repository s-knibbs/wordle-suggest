# Wordle Suggest
REPL program that provides suggestions to wordle clues.

## Usage
```
$ python wordle_suggest.py --help

usage: wordle_suggest.py [-h] [-w WORD_LIST] [-l WORD_LENGTH]

options:
  -h, --help            show this help message and exit
  -w WORD_LIST, --word-list WORD_LIST
                        Path to word list
  -l WORD_LENGTH, --word-length WORD_LENGTH
                        Length of words

The program operates as a REPL. Enter clues in the format 'GUESS:PRESENT:MATCHES', example
'slate:a:0s3t'. The number of possible answers will decrease as each clue is entered. Use CTRL+D to
reset the answers. CTRL+C to exit.
```

**Note**: Word list is only optional if you have the `wbritish-large` debian package installed since this is used as the default.

## Example output

```
8658 answers> slate:a:3t
agita  akita  amity  anita  aorta  aunty
azoth  bantu  barth  batty  biota  cacti
canto  cantu  canty  catty  chita  cotta
darth  dicta  faith  fanti  fatty  garth
gotta  gupta  gutta  haiti  horta  junta
manta  marta  marti  marty  nafta  natty
outta  panto  panty  party  patti  patty
pinta  pitta  quota  ratty  tanta  tanto
tartu  tarty  tatty  vitta  warta  warty
54 answers> 
```