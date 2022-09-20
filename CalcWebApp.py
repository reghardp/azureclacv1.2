import os
import sys
from flask import Flask, request, redirect, render_template, url_for, g
import flask 
from werkzeug.utils import secure_filename
from azure.storage.blob import BlockBlobService
import string, random, requests
from pathlib import Path
import time
import jinja2
import logging

app = Flask(__name__, instance_relative_config=True)

# app.config.from_pyfile('config.py')
# account = app.config['ACCOUNT']   # Azure account name
# key = app.config['STORAGE_KEY']      # Azure Storage account access key  
# container = app.config['CONTAINER'] # Container name

account = "autopricing"   # Azure account name
key = "z+hBvJzSDUokiPxKfiSbxcWdMwgtG0ftlcZubzvl3TzXzYX+SDe8JDA1ypboL0fcFrxPp+vpJSR6+AStdT+4Fw=="     # Azure Storage account access key  
container = "excel-input" # Container name

STORAGEACCOUNTURL = "https://autopricing.blob.core.windows.net"
STORAGEACCOUNTNAME = "autopricing"
STORAGEACCOUNTKEY = "z+hBvJzSDUokiPxKfiSbxcWdMwgtG0ftlcZubzvl3TzXzYX+SDe8JDA1ypboL0fcFrxPp+vpJSR6+AStdT+4Fw=="
CONTAINERNAME = "template"
TEMPLATENAME = "Famous_Brands_VM.xlsx"
OUTPUTFILE = "Costing_Output"

blob_service = BlockBlobService(account_name=account, account_key=key)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      if request.form['btn_identifier'] == "upload_template":
         file = request.files['file']
         filename = secure_filename(file.filename)
         fileextension = filename.rsplit('.',1)[1]
         Randomfilename = id_generator()
         filename = Randomfilename + '.' + fileextension
         try:
            blob_service.create_blob_from_stream(container, filename, file)
            # render_template("home.html", uploaded=1, download_ready=0)
            with open("filename.txt", "w", encoding='utf-8') as file:
               file.write(filename)
            for i in range(10):
               done = ifblob_exists(filename)
               if done:
                  print("\t Blob exists :" + " " + filename)
                  return render_template("home.html", uploaded=1, download_ready=1)
               else:
                  print("\t Blob does not exists :" + " " + filename)
                  # render_template("home.html", uploaded=1, download_ready=0)
                  time.sleep(15)

         except Exception:
            print('Exception=' + Exception)
            pass
         return render_template("home.html", uploaded=1, download_ready=0)
         # 
         # ref =  'http://'+ account + '.blob.core.windows.net/' + container + '/' + filename
         # return render_template("uploaded.html")
      if request.form['btn_identifier'] == "download_template":
         local_path = str(Path.home() / "Downloads")
         container_name = CONTAINERNAME 
         local_file_name  = TEMPLATENAME
         full_path_to_file = os.path.join(local_path, local_file_name)
         blob_service.get_blob_to_path(container_name, local_file_name, full_path_to_file)

      if request.form['btn_identifier'] == "download_output":
         local_path = str(Path.home() / "Downloads")
         with open("filename.txt", "r" , encoding='utf-8') as file:
            filename = file.readlines()
            print(filename)
         os.remove("filename.txt")   
         local_file_name  = filename[0]
         print(filename)
         container_name = 'out'
         block_blob_service = BlockBlobService(account_name='exportdata23', account_key='rbVxBcL3cGi7FBl5Jj0EacsDzGZ9GiFikGzMQeF6BPyyW3rrPLiJXW82M4s21iJDC0+66l2Ywsim+AStwj3KDA==', socket_timeout=60)
         full_path_to_file = os.path.join(local_path, local_file_name)
         block_blob_service.get_blob_to_path(container_name, local_file_name, full_path_to_file)
   
   return render_template("home.html", uploaded = 1 , download_ready = 0 )
   
   # return render_template('index.html')

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def ifblob_exists(filename):
   try:
      container_name = 'out'
      block_blob_service = BlockBlobService(account_name='exportdata23', account_key='rbVxBcL3cGi7FBl5Jj0EacsDzGZ9GiFikGzMQeF6BPyyW3rrPLiJXW82M4s21iJDC0+66l2Ywsim+AStwj3KDA==', socket_timeout=60)
      isExist = block_blob_service.exists(container_name, filename)
      if isExist:
         return True
      else:
         return False
   except Exception:
      print('Not found')
      
if __name__ == '__main__':
    app.run()



# from flask import Flask, render_template, request
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# # @app.route("/")
# # def home():
# #     return    


# @app.route('/upload')
# def upload_file():
#    return render_template('upload.html')
	
# @app.route('/uploader', methods = ['GET', 'POST'])
# def uploaded_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'


# if __name__ == "__main__":
#     app.run()

#     CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=autopricing;AccountKey=z+hBvJzSDUokiPxKfiSbxcWdMwgtG0ftlcZubzvl3TzXzYX+SDe8JDA1ypboL0fcFrxPp+vpJSR6+AStdT+4Fw==;EndpointSuffix=core.windows.net"

#     CONTAINER_NAME = "excel-input"

#     output = df.to_csv(index_label="idx", encoding = "utf-8")

#     output_blob_name = "output_blob3.csv"

#     container_client = ContainerClient.from_connection_string(conn_str=CONNECT_STR, container_name=CONTAINER_NAME)

#from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


