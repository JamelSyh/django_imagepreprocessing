
from .models import Image
from .serializers import ImageSerializer, ProcessingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import shutil
from django.shortcuts import get_object_or_404


from internship import *
import cv2 as cv


def path(path):
    return ".{}".format(path)


def resPath(name):
    return "./media/images/results/{}.png".format(name)


def read(img):
    image_path = path(img)
    image = cv.imread(image_path)
    return image


def show(img):
    cv.imshow("img", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def write(img, name):
    image_path = resPath(name)
    cv.imwrite(image_path, img)

# Create your views here.


@api_view(['GET', 'POST'])
def post(req):
    try:
        image = Image.objects.get(pk=1)
    except:
        image = None
    if (image):
        serializer = ImageSerializer(instance=image, data=req.data)
    else:
        serializer = ImageSerializer(data=req.data)

    if serializer.is_valid():
        folder = 'media/images/base'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        serializer.save()
        if (serializer.data['type'] == "0"):
            path = f"/media/images/base/{serializer.data['title']}.png"
            im = read(path)
            path2 = f"./media/images/base/{serializer.data['title']}.png"
            gim = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            cv.imwrite(path2, gim)

    return Response(serializer.data)


list = [None, Binarization.globalFixed, Binarization.otsu, Binarization.multi,
        Binarization.sauvola, Binarization.niblack, Binarization.mean, Binarization.gaussian, Filter.canny, Filter.sobel, Filter.laplacian, Filter.median, Filter.gaussian, Morphology.dilation, Morphology.erosion]


@api_view(['GET', 'POST'])
def result(req):
    image = Image.objects.get(pk=1)
    serializer = ProcessingSerializer(data=req.data)
    if serializer.is_valid():
        # serializer.save()
        im = read(f"/media/images/base/{image.title}.png")
        result = Processing(
            im, list[int(serializer.data['type1'])], list[int(serializer.data['type2'])], list[int(serializer.data['type3'])], thresh=int(serializer.data['thresh']), kernel=int(serializer.data['kernel']), c=float(serializer.data['c']), k=float(serializer.data['k'])).result()
        folder = 'media/images/results'

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        name = f"{serializer.data['type1']}{serializer.data['type2']}{serializer.data['type3']}{serializer.data['thresh']}{serializer.data['kernel']}{serializer.data['c']}{serializer.data['k']}"
        write(
            result, name)

    return Response({'image': "/media/images/results/{}.png".format(name)})
