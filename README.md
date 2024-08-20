# bridge
Statistical analysis of the card game bridge


todo: make better faster stronger

# setup

pull package
`cd bridge-solver && make && cd -`

# example commands:

most basic command, generate and count inversions for new hands:
`python3 bridge2.py -n {NUM_HANDS}`

to save to a file add `-s flag` like so
`python3 bridge2.py -n {NUM_HANDS} -s {file/path}`

to load from a file (minimal checks that it is properly formatted):
`python3 bridge2.py -l {file/path}`

`-t` flag will let you set more threads for the hand generation process

I often use this to generate a new hand:
`python3 bridge2.py -n 500 -s HandRecords/test.csv -t 16`

and then this when i'm focusing on the processing not the generation
`python3 bridge2.py -l HandRecords/test.csv`