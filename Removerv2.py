#################################################################
#       Import and Read.me and TO DO                            #
#################################################################
import os, time     # voor bekijken van foto's nieuwe te plaatsen in de dir en oude te verwijderen
import sys          # zelfde als OS
import tkinter as tk       # TODO nog een frame voor HURRY mode en eentje voor chill mode
from PIL import ImageTk,Image      # pil is de MAIN functie voor BGRWHITE
import numpy as np                  # voor beide BGR2WHITE
import cv2                          # Dit is voor BGR2WHITE

HEIGHT = 600                        # Voor TKinter frames
WIDTH = 800                         # Voor TKinter frames
#################################################################
#               Read.me                                         #
#  bgrwhite heeft een 80% success rate op foto die niet witte   #
#  Product kleur hebben heeft het plaatje een witte achtergrond #
#  dan is het best om de andere mogelijkhijd te gebruiken       #
#  Bgr2White, deze heeft een 20% maar dit werkt geweldig op     #
#  plaatjes met een witte product kleur                         #
#                                                               #
#   Copyright Hugo van Geijn 06-05-2020                         #
#################################################################

#################################################################
#                   80% success rate                            #
#################################################################


def bgrwhite(foto):
    # vars voor de input output maken van de foto's 
    text = "./input/" + foto
    temp = "./TEMP/" + foto
    img = Image.open(text).convert("RGB")
    img.save(temp)
    pixels = img.load() # maak de pixel map om te zoeken voor de pixel
    #if r > 233 and g > 233 and b > 233:
    for i in range(img.size[0]): # voor elke pixel in de foto doe:
        for j in range(img.size[1]):
            # hier splitmatrix naar RGB dan evalueer elke pixel of ze hoger zijn dan VAR
            if pixels[i,j][0] >220 and pixels[i,j][1] > 220 and pixels[i,j][2] > 220:
            # verander deze RGB voor een andere kleur
                pixels[i,j] = (256, 256 ,256)
            
    nfoto = "./output/" + foto 
    img.save(nfoto)
    os.remove("./input/" + foto)

def doOnePicture(picture):
    bgrwhite("./input/")

def allpicslazy():
    for geladenfile in os.listdir("./input"):
        print(geladenfile)
        bgrwhite(geladenfile)

#########################################################
###        20% success rate vooral bij model foto's   ###
#########################################################

def bgr2white(foto):
    
    text = "./input/" + foto
    #== Parameters niet aan kloten ===================================================
    BLUR = 21
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 200
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (1.0,1.0,1.0) # In BGR format < (1.0,1.0,1.0) voor wit (0.1, 0.1, 0.1) voor zwart
    #####################################################################################
    # Processing image to mask   #

    #-- lees foto ---------------------------------------------------------------------
    img = cv2.imread(text)
    #maakt snel een TEMP foto
    temp = cv2.imwrite("./TEMP/" + foto, img)
    print("foto " + foto + " geladen")
    row,col = img.shape[:2]
    bottom = img[row-2:row, 0:col]
    mean = cv2.mean(bottom)[0]

    bordersize = 100
    border = cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[255, 255, 255])
    gray = cv2.cvtColor(border,cv2.COLOR_BGR2GRAY)

    #-- Edge Detectie -------------------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    
    #-- vind contouren in edges, sorteer via area ----------------------------------------
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # als je oude CV2 Gebruikt werkt dit niet

    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    #-- maakt een lege MASK, maakt polygons in de MASK ----
    # Mask is zwart, polygon is wit
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    #-- Smooth mask, dan blur --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    border         = border.astype('float32') / 255.0           #  for easy blending

    masked = (mask_stack * border) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 
    
    badstring = "./input/"
    foto.replace(".", "")
    foto.replace("/", "")
    foto.replace("input", "")

    #zet de nieuwe foto in de output
    newfoto = "./output/" + foto
    newfile = cv2.imwrite(newfoto, masked)
    
    # verwijder img van input 
    os.remove("./input/" + foto)

def allpicsexp():
    for geladenfile in os.listdir("./input"):
        print(geladenfile)
        bgrwhite(geladenfile)

        
filearray = []
#Loop
i = 0
#TODO frame voor SNELHEIDDDDDDDD


def dysWindow():
    def refreshimg():
    
        load = Image.open("./input/" + filearray[1])
        render = ImageTk.PhotoImage(load)
        img.configure(image=render)


    root = tk.Toplevel(app)
    root.title("keuzemenu")
    #laad de foto in
   
    for geladenfile in os.listdir("./input"):
        filearray.append(geladenfile)
    load = Image.open("./input/" + filearray[0])
    render = ImageTk.PhotoImage(load)

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="#80c1ff")
    canvas.pack()

    frame = tk.Frame(root, bg="#80c1ff",bd=5, cursor="arrow")
    frame.place(relx=0.5,rely=0.1,relwidth=0.75,relheight=0.1,anchor="n")

    entry = tk.Entry(frame,bg="white", font=40)
    entry.place(relwidth=0.65,relheight=1)

    but1 = tk.Button(frame, text="grijs naar wit",font=1,command=lambda: bgrwhite(geladenfile))
    but1.place(relx=0.7,relheight=1,relwidth=0.3)
    but2 = tk.Button(frame, text="MASK",font=1,command=lambda: bgr2white(geladenfile))
    but2.place(relx=0.4,relheight=1,relwidth=0.3)
    but3 = tk.Button(frame, text="Refresg",font=1,command=refreshimg)
    but3.place(relx=0.1,relheight=1,relwidth=0.3)

    img = tk.Label(root, image=render)
    img.image = render
    img.place(relx=0.05, rely=0.25, relwidth=0.9 )






#############################################################################
#               TKinter frame voor keuze menu                               #
#############################################################################
app = tk.Tk()
app.title("Grey2White")
canvas = tk.Canvas(app, width=500, height=600)
canvas.pack()
frame = tk.Frame(canvas, bg="#80c1ff",bd=5, cursor="arrow", width=1000, height=1200)
frame.pack()

labelExample = tk.Label(frame,bg="#80c1ff", text = "Lazy Mode Succes:80%")
labelExample.pack()
buttonhint  = tk.Label(frame,bg="#80c1ff", text = "zorg dat er geen witte producten in de INPUT folder staan")
buttonhint.pack()
buttonExample = tk.Button(frame, text="Lazy button", command=allpicslazy)
buttonExample.pack()
labelwhite = tk.Label(frame,bg="#80c1ff", text= "")
labelwhite.pack()
labelexperimental = tk.Label(frame,bg="#80c1ff", text="Expirimentele modus Succes: 20%")
labelexperimental.pack()
labelexperimental2 =tk.Label(frame,bg="#80c1ff", text="te gebruiken bij foto's met model van ver")
labelexperimental2.pack()
buttonExp = tk.Button(frame, text="zorg dat er model foto's van afstand in staan", command=allpicsexp)
buttonExp.pack()
labelwhite2 = tk.Label(frame,bg="#80c1ff", text= "")
labelwhite2.pack()
labelDYS = tk.Label(frame,bg="#80c1ff", text="zelf kiezen per foto")
labelDYS.pack()
buttonDYS = tk.Button(frame, text="  DYS   ", command=dysWindow)
buttonDYS.pack()

app.mainloop()






# roep de functie uit
#bgrwhite("front-2.jpg")



