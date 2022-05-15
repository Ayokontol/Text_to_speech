from utils import prepare_text as pt
from sys import argv


if __name__ == '__main__':
    script, input_path = argv
    if input_path[:-3] == 'csv':
        pt.prepare_and_save_samples_from_csv(csv_name=input_path, path_to_samples_dir='/samples/')
    else:
        with open(input_path, 'r') as f:
            text = f.read()
        sample = pt.prepare_sample(text)
        file_name = input_path.split('/')[-1]
        pt.save_sample_to_file(sample, 'samples/' + file_name)

