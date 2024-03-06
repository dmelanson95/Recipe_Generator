from textgenrnn import textgenrnn
import tensorflow as tf
import os

textgen = textgenrnn(name='recipe_generator')

#location folder name of file containing csv dataset
folder = 'C:/Users/dpfab/Desktop/Senior Design Project/'
#file name in folder
ds_dest = 'recipes_dataset.csv'

os.chdir(folder)

textgen.train_from_file(file_path=folder+'ds_subset.csv', delim=',', new_model=True, is_csv=True, num_epochs=10, dropout=0.1,
                        rnn_bidirectional=True, rnn_layers=4, max_length=128, word_level=True, multi_gpu = True
                        )
print(f"Generated Text:\n\n{textgen.generate(temperature=0.1, return_as_list=True)}")
textgen.save(folder+'weights.hdf')

