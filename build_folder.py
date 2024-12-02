import shutil
import os


def build():
    out_dir = 'ccp_v2'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    subfolders = [f.path for f in os.scandir('repos') if f.is_dir()]
    for folder in subfolders:
        arr = os.listdir(folder)
        for f in arr:
            docs = os.listdir(os.path.join(folder, f))
            for doc in docs:
                if not os.path.exists(os.path.join(out_dir, doc)):
                    shutil.copy(os.path.join(os.path.join(folder, f), doc),
                                os.path.join('ccp_v2', doc)
                                )
                else:
                    i = 1
                    new_name = ''
                    while True:
                        new_name = os.path.join(out_dir, doc.split('.')[0] + '_' + str(i) + '.' + doc.split('.')[1])
                        i = i + 1
                        if not os.path.exists(new_name):
                            break
                    shutil.copy(os.path.join(os.path.join(folder, f), doc),
                                new_name
                                )
    print('Files in CCP_v2: ', len(os.listdir(out_dir)))
