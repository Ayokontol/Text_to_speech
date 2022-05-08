from utils import prepare_text as pt
import pandas as pd


def test():
    data = pd.read_csv('data/AN-1073-text.csv')['text']
    text = pt.prepare_sample(data[3])
    print(text)


if __name__ == '__main__':
    test()
    #pt.prepare_samples_from_csv(csv_name='data/AN-1073-text.csv', path_to_samples_dir='/samples/')
