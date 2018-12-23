from tkinter import filedialog
from tkinter import * 
from PIL import ImageTk
from PIL import Image  
import numpy as np 
import scipy.ndimage.filters as fi
root = Tk()
root.minsize(800,600)  

w_c, h_c = 700, 500
canvas = Canvas(root, width = w_c, height = h_c)   
canvas.pack()

#taking image as an input
def hello():
	filename = filedialog.askopenfilename(initialdir = "/home/nandan/Desktop",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
	global image
	global image_on_canvas
	global PIL_image
	image = Image.open(filename)
	image = image.convert('L') 

	[w, h] = image.size
	print(image)
	image = image.resize((600,600))
	img   = ImageTk.PhotoImage(image)

	image_on_canvas = canvas.create_image(0,0, anchor=NW, image=img)     
	canvas.mainloop()

# def save_img():
# 	# global PIL_image_display #defining global variable for latest output image
# 	## Uses tkFileDialog library to select an image file
# 	savedimage = filedialog.asksaveasfilename(initialdir='/home/nandan/Desktop',title='Choose image file',filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
# 	PIL_image.save(savedimage,"JPEG") ##saves image in jpeg format to selected file

def quit(event):                           
    print("Double Click, so let's stop") 
    import sys; sys.exit() 

#function to convolve
def Convolve(box, image_to_convolve):

	n,s = box.shape
	h, w = image_to_convolve.shape[:2]
	img_pad = np.pad(image_to_convolve, ((n//2,n//2),(n//2,n//2)), 'constant')
	for j in range(0,h):
		for i in range(0,w):
			image_to_convolve[j,i] = np.sum(img_pad[(j):(j+n), (i):(i+n)]*box)

	return image_to_convolve

#Function for Gamma correction
def Gamma():
	def show_entry_fields():
		gamma_value = entry_1.get()
		g = float(gamma_value)
		
		img_g = np.asarray(image, dtype=float)
		img_g = img_g/255

		print(gamma_value,img_g)
		gamma_corrected = (img_g**g)
		gamma_corrected = gamma_corrected*255
		PIL_image = Image.fromarray(np.uint8(gamma_corrected))
		PIL_image_display   = ImageTk.PhotoImage(PIL_image)

		canvas.itemconfig(image_on_canvas, image = PIL_image_display)
		canvas.mainloop()

	label1 = Label(root, text='Gamma_value')
	label1.pack()
	entry_1 = Entry(root)
	entry_1.pack()
	Button(root, text='Show', command=show_entry_fields).pack()
	return entry_1.get()

#Fuction for gaussian blurr
def Gaussian_Blurr():
	def Act_Blurr():
		value = entry_2.get()
		image_blur = np.array(image)
		# image_blur = image_blur.copy()
		n = 2*(int(value)) + 1
		h, w = image_blur.shape[:2]

		img_pad = np.pad(image_blur, ((n//2,n//2),(n//2,n//2)), 'constant') 
		box = (np.zeros((n,n)) + 1)/n**2

		image_blur2 = Convolve(box, image_blur)	
		PIL_image = Image.fromarray(np.uint8(image_blur2))
		PIL_image_display = ImageTk.PhotoImage(PIL_image)
		canvas.itemconfig(image_on_canvas, image = PIL_image_display)
		canvas.mainloop()

	label1 = Label(root, text='Gaussian_Blurr')
	label1.pack()	
	entry_2 = Entry(root)
	entry_2.pack()
	b = Button(root, text='Show', command=Act_Blurr).pack()

	return entry_2.get()

#Sharpening the image 
def Sharpening():
	def Act_sharpening():
		window_size = int(entry_3.get())
		
		std_space = 5 # entry_4.get()
		image_sharp = np.asarray(image,dtype=float)
		gaussianfilter_size = 2*(int(window_size)) + 1 #size of the gaussian filter
		
		# spatial_mask = gkern2(gaussianfilter_size, std_space)
		spatial_mask = np.zeros((gaussianfilter_size, gaussianfilter_size), dtype = float)
		for i in range(0,gaussianfilter_size): 
			for j in range(0, gaussianfilter_size):
				spatial_mask[i,j] = (0.3984/std_space)* np.exp(float(-np.square(i-window_size)-np.square(j-window_size))/float(2*std_space**2))            

		gaussianImage = Convolve(spatial_mask,image_sharp)
	
		diff = image - gaussianImage
		sharp = image + diff
		sharp = (sharp-np.amin(sharp))*255/np.amax(sharp)
		PIL_image = Image.fromarray(np.uint8(sharp))
		PIL_image_display = ImageTk.PhotoImage(PIL_image)
		canvas.itemconfig(image_on_canvas, image = PIL_image_display)
		canvas.mainloop()	
	
	
	label2 = Label(root, text='Gaussian_Blurr')
	label2.pack()
	entry_3 = Entry(root)
	entry_3.pack()
	b = Button(root, text='Show', command=Act_sharpening).pack()

#function for histogram equalization
def Hist_Equal():

	image_Hist = np.asarray(image)
	hist, bins = np.histogram(image_Hist, bins = 256,normed=True)
	CDF = np.cumsum(hist)*255

	cdf_m = np.ma.masked_equal(CDF,0)
	cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())

	cdf = np.ma.filled(cdf_m,0).astype('float')
	image_Hist = np.rint(image_Hist).astype(int)

	image_Hist = cdf[image_Hist]
	# hist2, bins2 = np.histogram(img2, bins = 256,normed=True)
	PIL_image = Image.fromarray(np.uint8(image_Hist))
	PIL_image_display = ImageTk.PhotoImage(PIL_image)
	canvas.itemconfig(image_on_canvas, image = PIL_image_display)
	canvas.mainloop()
	
#function performing log transformation
def log_transform():

	image_log = np.asarray(image)
	image_log = image_log/255
	image_log.astype(dtype =float)
	image_log = 1*(np.log10(image_log + 1))*255
	PIL_image = Image.fromarray(np.uint8(image_log))
	PIL_image_display = ImageTk.PhotoImage(PIL_image)
	canvas.itemconfig(image_on_canvas, image = PIL_image_display)
	canvas.mainloop()

#setting up the User Interface
menu = Menu(root)
root.config(menu=menu)

submenu1 = Menu(menu)

menu.add_cascade(label="File", menu=submenu1)
submenu1.add_command(label="New_image", command=hello)
submenu1.bind("<Button-1>", hello)
# submenu1.add_command(label="Save_image", command= save_img)
# submenu1.bind("<Button-1>", save_img)
# editmenu = Menu(menu)
editmenu1 = Menu(menu)

menu.add_cascade(label="Edit", menu=editmenu1)	
editmenu1.add_command(label="Gamma_correction", command=Gamma)
editmenu1.add_command(label="Histogram_Equalization", command=Hist_Equal)
editmenu1.bind("<Button-1>", Hist_Equal)
editmenu1.add_command(label="Log_Transform", command=log_transform)
editmenu1.bind("<Button-1>", log_transform)
editmenu1.add_command(label="Blurr", command=Gaussian_Blurr)
editmenu1.bind("<Button-1>", Gaussian_Blurr)
editmenu1.add_command(label="Sharpen", command=Sharpening)
editmenu1.bind("<Button-1>", Sharpening)


root.mainloop()
