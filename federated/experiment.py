from pathlib import Path
from datetime import datetime
import shutil
import os
import stat

class Experiment:
  def __init__(self, experiments_folder,experiment_name,create_new=True):
    self.name = experiment_name
    self.experiments_folder = experiments_folder
    self.create_new = create_new
    
    self.create_folder()
    
      
    
  def create_folder(self):
      # Salve a máscara atual
      old_mask = os.umask(0o000)

      self.now = datetime.now()
      if self.create_new:
        today_str = self.now.strftime("%Y_%m_%d_")
        self.path = f"{self.experiments_folder}/{today_str}{self.name}"
      else:
        self.path = f"{self.experiments_folder}/{self.name}"
      Path(self.path).mkdir(parents=True, exist_ok=True)

      # Altere as permissões da pasta para 777
      os.chmod(self.path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

      # Restaure a máscara original
      os.umask(old_mask)
      
      
  def change_permissions(self):
    # Salve a máscara atual
    old_mask = os.umask(0o000)

    for root, dirs, files in os.walk(self.path):
        for file in files:
            path = os.path.join(root, file)
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    # Restaure a máscara original
    os.umask(old_mask)
  
  def getFileName(self,extension=".log"):
    now_str = self.now.strftime("%Hh%Mm%Ss")
    return f"{self.path}/{now_str}{self.name}{extension}"
  
  def copyFileToExperimentFolder(self,file_name=''):
    shutil.copyfile(file_name, self.getFileName(extension=f".{file_name.split('.')[1]}"))