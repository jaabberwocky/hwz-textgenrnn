from textgenrnn import textgenrnn
import sys
import os

if len(sys.argv) != 3:
    raise Exception("Incorrect number of commandline arguments.")
else:
    trainFilePath = sys.argv[1]
    num_epochs = sys.argv[2]

textgen = textgenrnn()
textgen.train_from_file(trainFilePath, num_epochs = num_epochs, verbose = 1)
if os.path.isfile('textgenmodel_saved.hdf5'):
    os.remove('textgenmodel_saved.hdf5')
textgen.save('textgenmodel_saved.hdf5')
