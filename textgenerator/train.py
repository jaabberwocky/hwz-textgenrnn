from textgenrnn import textgenrnn
import sys
import os
import datetime
import uuid

if len(sys.argv) != 3:
    raise Exception("Incorrect number of commandline arguments.")
else:
    trainFilePath = sys.argv[1]
    num_epochs = sys.argv[2]

textgen = textgenrnn()
textgen.train_from_file(trainFilePath, num_epochs = num_epochs, verbose = 1)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
filename = 'textgenmodel_saved_%s.hdf5' % timestamp
try:
    if os.path.isfile(filename):
        os.remove(filename)
    textgen.save('textgenmodel_saved.hdf5')
except:
    textgen.save(str(uuid.uuid4())+".hdf5")
