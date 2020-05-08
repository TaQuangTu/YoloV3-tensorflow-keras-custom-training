# YoloV3-tensorflow-keras-custom-training
A tutorial for training YoloV3 model with `KAIST` data set. This tutorial try to help you train YoloV3 model on Google Colab in a short time.
</br>**<h2>Steps:</h2>**</br>
1. Clone this repository and upload the project to your `Google Drive`
2. Create a new Google Colab and `Mount Drive`
3. Get in your project on Drive and download dependances:
</br> * Example: `%cd /content/drive/My Drive/Colab Notebooks/final/YOLOv3-custom-training`
<br> * Download dependances for the project - Run: `!pip install -r requirements.py`
2. Download YOLOv3 weights from YOLO website, or use wget command:
* `wget https://pjreddie.com/media/files/yolov3.weights`. You can also simply download it by clicking to the url 
* Copy downloaded weights file to `model_data` folder.
3. Convert the Darknet YOLO model to a Keras model:
<br>Open file `convert.py`<br>
* Change `weights_path` variable to the weights file you have already downloaded at a moment ago.<br>
* Run command: `!python convert.py`
4. Prepare your dataset
<br> Push data set up to `dataset` folder:
<br>
   Project<br>
      --dataset<br>
        annotations.zip<br>
        set00.zip<br>
        set01.zip<br>
        set02.zip<br>
        ..<br>
        set11.zip<br>
<br>
5. Now you need create `annotation file` to train, each line in the file will present an image and has format likes following:
<br>

    dataset/images/set01/V004/visible/I01283.jpg 291,237,335,312,0 499,238,552,358,0 541,249,586,348,0 580,220,628,313,2 
    dataset/images/set01/V004/visible/I00242.jpg 238,211,258,247,2 
    dataset/images/set01/V004/visible/I01390.jpg 
    dataset/images/set01/V004/visible/I01385.jpg 
    dataset/images/set01/V004/visible/I00934.jpg 
    dataset/images/set01/V004/visible/I00983.jpg 
    dataset/images/set01/V004/visible/I00427.jpg 
    dataset/images/set01/V004/visible/I01308.jpg 133,232,177,307,0 393,231,450,355,0 425,241,472,351,0 414,218,467,317,2 
    dataset/images/set01/V004/visible/I01317.jpg 62,232,111,314,0 338,229,395,353,0 363,240,416,351,0 351,219,405,319,2 
    dataset/images/set01/V004/visible/I00647.jpg 
    dataset/images/set01/V004/visible/I01300.jpg 188,233,232,308,0 434,231,491,355,0 470,240,515,346,0 469,218,518,313,2 
    
    
<br>

Line format = `image_path+' '+xmin,ymin,xmax,ymax,class_label+' '+(more if the image has more than one object)`
<br> I have created and named the file `4_CLASS_test.txt`
<br> You also need a class names file, I created it already - `4_CLASS_test_classes.txt` likes below:<br>

      person
      people
      cyclist
      person?


6. extract dataset zip files to colab temperary folder named `sample_data` for faster training (than training with dataset inside driver)<br>
<br> Run: `!python extract.py`
<br>Make sure folder tree be like: <br>
sample_data:<br>
  --dataset:<br>
    --annotations:<br>
      --set00<br>
      --set01<br>
      --set02<br>
      --set03<br>
      --set04<br>
      --set05<br>
      ...<br>
      --set11<br>
    --images<br>
      --set00<br>
      --set01<br>
      --set02<br>
      ...<br>
      --set11<br>
<br>
7. Train
<br> Look into `train.py` file, on `create_model` method call, change parameter 'weights_path' to the weight file which has been downloaded a moment ago.
<br> Run: `!python train.py`
