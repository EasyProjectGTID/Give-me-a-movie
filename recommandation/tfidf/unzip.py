import os, zipfile
import shutil

folder = '/home/hadrien/Bureau/sous-titres'
extension = ".zip"

def allUnzip():
    for path, dir_list, file_list in os.walk(folder):
        print(file_list)
        for file_name in file_list:

            if file_name.endswith(".zip"):
                try:
                    abs_file_path = os.path.join(path, file_name)

                    # The following three lines of code are only useful if
                    # a. the zip file is to unzipped in it's parent folder and
                    # b. inside the folder of the same name as the file

                    parent_path = os.path.split(abs_file_path)[0]
                    output_folder_name = os.path.splitext(abs_file_path)[0]
                    output_path = os.path.join(parent_path, output_folder_name)

                    zip_obj = zipfile.ZipFile(abs_file_path, 'r')
                    zip_obj.extractall(output_path)
                    zip_obj.close()
                except:
                    pass



