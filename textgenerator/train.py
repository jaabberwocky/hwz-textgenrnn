from textgenrnn import textgenrnn
import sys
import os

if len(sys.argv) != 2:
    raise Exception("Incorrect number of commandline arguments.")
else:
    trainFilePath = sys.argv[1]

textgen = textgenrnn()
textgen.train_from_file(trainFilePath, num_epochs = 1, batch_size = 512)
if os.path.isfile('textgenmodel_saved.hdf5'):
    os.remove('textgenmodel_saved.hdf5')
textgen.save('textgenmodel_saved.hdf5')
