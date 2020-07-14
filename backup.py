#! python3

import os
import shutil
import time

def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


timestr = time.strftime("%Y%m%d")
backupFolderPath = '/media/sf_VirtualMachineFileShare/AuctionHouseData/Builds'
destination = backupFolderPath + '/' + timestr


copy_and_overwrite('./', destination)







