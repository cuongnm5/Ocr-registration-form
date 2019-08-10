import cv2
import img2pdf 
from PIL import Image 
import os
import io

class Solve(object):
    def writing(self, IMG_PATH, text, font_size):
        image = cv2.imread(IMG_PATH)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, text, (300, 300), font, font_size, (0, 0, 0), 2)
        cv2.imshow('image',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def list_img2PDF(self):
        from fpdf import FPDF
        pdf = FPDF()
        # imagelist is the list with all image filenames
        imagelist = []
        imagelist.append("/home/dodo/Pictures/bill4.jpg")
        imagelist.append("/home/dodo/Pictures/bill4.jpg")
        pdf.add_page()
        for image in imagelist:
            # pdf.add_page()
            pdf.image(image)
        pdf.output("yourfile.pdf", "F")

    def image2PDF(self):
        # storing image path 
        img_path = "/home/dodo/Pictures/bill4.jpg"
        
        # storing pdf path 
        pdf_path = "/home/dodo/Pictures/test.pdf"
        
        # opening image 
        image = Image.open(img_path)
        
        # converting into chunks using img2pdf 
        pdf_bytes = img2pdf.convert(image.filename) 
        
        # opening or creating pdf file 
        file = open(pdf_path, "wb") 
        
        # writing pdf files with chunks 
        file.write(pdf_bytes) 
        
        # closing image file 
        image.close() 
        
        # closing pdf file 
        file.close() 
        
        # output 
        print("Successfully made pdf file") 


if __name__ == "__main__":
    test = Solve()
    # test.list_img2PDF()
    test.writing("/home/dodo/Pictures/test.png","haha",20)