# Extract train dataset
from zipfile import ZipFile

zip_files = [ 'dataset/annotations.zip','dataset/set00.zip', 'dataset/set01.zip', 'dataset/set02.zip', 'dataset/set03.zip', 'dataset/set04.zip',
             'dataset/set05.zip']

des_dir = '/content/sample_data/dataset/images'
des_dirs = ['/content/sample_data/dataset',des_dir + '/set00', des_dir + '/set01', des_dir + '/set02', des_dir + '/set03', des_dir + '/set04',
            des_dir + '/set05']
for index, zip_path in enumerate(zip_files):
    with ZipFile(zip_path, 'r') as z:
        print("extracting..", zip_path)
        z.extractall(path=des_dirs[index])
