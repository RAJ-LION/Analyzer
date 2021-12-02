import tkinter as tk
import pickle
import re 
import nltk
from PIL import ImageTk,Image
from tkinter import filedialog, Text
from multiprocessing import Process
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from io import StringIO
import os


root = tk.Tk()
app = []

def addApp():

   

    filename= filedialog.askopenfilename(initialdir="/", title="Select File",
                                         filetypes=(("Pdf files",".pdf"), ("all files", "*.*")))
    app.append(filename)
    print(filename)
    print("Okay! The file has been selected. Kindly click 'Analyse pdf' button to check its Goals Accuracy ! \n\n\n\n")
   

def convert_pdf_to_str(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text
        

def runApps():
    
    text = convert_pdf_to_str(app[0])
    text = str(text)
    text = re.sub('\s+', ' ', text)
    a = set(nltk.corpus.stopwords.words('english'))

    text1 = nltk.word_tokenize(text.lower())
    stopwords = [x for x in text1 if x not in a]
    text = nltk.word_tokenize(" ".join(map(str, stopwords)))
    finaltext = ''

    for token in text:
        if(nltk.pos_tag([token])[0][1] == 'JJ' or nltk.pos_tag([token])[0][1] == 'NN' or nltk.pos_tag([token])[0][1][0] == 'V'):
          finaltext += " "+nltk.pos_tag([token])[0][0]
   
    
    pickle_in = open("classifier.pkl", "rb")
    classifier = pickle.load(pickle_in)
    prediction = classifier.predict_proba([finaltext])
    li = []
    for x in prediction[0]:
        li.append(x)
    goals = ['No Poverty', 'Zero Hunger', 'Good Health and Well-Being',
                'Quality Education', 'Gender Equality', 'Clean Water And Sanitation', 'Affordable Clean Energy',
                'Decent Work And Economic Growth', 'Industry,Innovation And Infrastructure', 'Reduced Inqualities',
                'Sustainable Cities And Communities', 'Responsible Consumption And Production', 'Climate Action', 'Life Below Earth', 'Life on Land']
    final = ''
    count = 0
    temp1 = ""
    temp2 = ""
    temp3 = "-"

    li1 = li.copy()
    li1.sort(reverse=True)
    for x in li1:
        temp = li.index(x)
        temp1 = str(temp+1)
        if(temp < 9):
            temp1 = "0"+str(temp+1)
        temp2 = str(count+1)
        if(count < 9):
            temp2 = "0"+str(count+1)
        temp3 = ' '
        final += "|"+temp2+". "+temp1+" - " + \
            str(goals[temp])+temp3+"=>\t"+str(x) 
            
        final += '\n'
        count += 1

    print("RANKINGS: \n")
    print(final)
    app.clear()   
       
       

root.title("RAJ-ANALYSER")
canvas = tk.Canvas(root, height=290,width=250)
canvas.pack()
img = ImageTk.PhotoImage(Image.open("swami.jpg"))
canvas.create_image(130, 200, image=img)


openFile= tk.Button(root, text="Browse your PDF", padx=10,
                    pady=5, fg="white", bg="#263D42", command=addApp)
openFile.pack()

runApps= tk.Button(root, text="Analyse PDF", padx=10,
                    pady=5, fg="white", bg="#263D42", command=runApps)
runApps.pack()
root.mainloop()




