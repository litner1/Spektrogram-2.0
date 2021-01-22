import tkinter as tk
import io
import sounddevice as sd
from scipy.io import wavfile
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import SpanSelector
from matplotlib import pyplot as pltx
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib import pyplot as plt
import numpy as np





class Aplikacja(tk.Frame):
      
    frequency = 44100
    seconds = 3
    filename = "test11.wav"
   
    def __init__(self, parent):
       

        #menu gorne
        tk.Frame.__init__(self, parent)
        self.parent = parent
        menubar = tk.Menu(self)
        submenu1 = tk.Menu(menubar, tearoff=0)
        submenu1.add_command(label="Nagraj", command=lambda:self.record())
        #submenu1.add_separator()

        submenu1.add_command(label="Odtwórz", command=lambda:self.play(self.filename))
        submenu1.add_command(label="Narysuj", command=lambda:self.plot(self.filename))
        #submenu1.add_separator()
        menubar.add_cascade(label="Plik", menu=submenu1)
        self.parent.config(menu=menubar)

        self.upper_figure = Figure(linewidth=5, edgecolor = '#00FF00')
        self.upper_canvas = FigureCanvasTkAgg(self.upper_figure, master=self)
        self.upper_canvas.get_tk_widget().place(x=50, y=10, width=700, height=400)
        self.upper_toolbar = NavigationToolbar2Tk(self.upper_canvas,self) 
        self.upper_toolbar.place_configure(x=50, y=420)
        self.upper_canvas.draw()


        self.lower_figure = Figure(linewidth=5, edgecolor = '#FF0000')
        self.lower_canvas = FigureCanvasTkAgg(self.lower_figure, master=self) 
        self.lower_canvas.get_tk_widget().place(x=50, y=510, width=600, height=200) # umieszczamy tkinterowy widget (get_tk_widget()) danej kanwy na oknie
        self.lower_toolbar = NavigationToolbar2Tk(self.lower_canvas,self) 
        self.lower_toolbar.place_configure(x=50, y=720)
        self.lower_canvas.draw()




        self.pack(side="top", fill="both", expand=True) # umieszczamy naszą ramkę zdefiniowaną przez klasę  w oknie aplikacji

    def plot_input(self, channel):
        #plt.figure()
        #plt.title('Plik dźwiękowy')
        #plt.plot(channel)
        #plt.xlabel('Próbki')
        #plt.ylabel('Amplituda')
        #plt.show(block=False)
        
        self.upper_figure.clear()
        chart = self.upper_figure.add_subplot(111)
        chart.plot(channel)
        print(type(chart))
        chart.set_xlim(0,self.seconds*self.frequency)
        chart.set_xlabel('Próbki')
        chart.set_ylabel('Amplituda')
        chart.set_title('Plik dźwiękowy')

        
        
        chart.set_xticks([(i/10*len(channel)) for i in range(11)])
        chart.set_xticklabels([(i/10*len(channel))/self.frequency for i in range(11)])

        self.upper_canvas.draw()


    def plot_spektogram(self, channel):
      
        #plt.figure()
        #a, b, c, image  = d.specgram(channel, NFFT= 1024, Fs=self.frequency, scale_by_freq=True, noverlap=200)
        #plt.title('Spektrogram')
        #plt.colorbar(image)
        #plt.ylabel('Częstotliwość [Hz]')
        #plt.xlabel('Czas [sec]')
        #plt.ylim(0,self.frequency/2)
        #plt.show(block=False)

        self.lower_figure.clear()
        chart = self.lower_figure.add_subplot(111)
        a, b, c, image  = chart.specgram(channel, NFFT= 2048, Fs=self.frequency, scale_by_freq=True, noverlap=2000)
        chart.set_xlabel('Sekundy')
        chart.set_ylabel('Częstotliwość [HZ]')
        chart.set_title('Spektrogram')
        self.lower_figure.colorbar(image)
        self.lower_canvas.draw()



    def plot(self, file_name):

        freq, data = wavfile.read(file_name)
        if len(data.shape) == 1:
           channel = data[:]
           print("plik mono")
           print(data.shape)
        else:
           channel = data[:,0]
           print("plik stereo")
           print(data.shape)

        samples = data.shape[0]
        seconds = samples / freq
        sample_time = 1.0 / freq
        print("próbki ", samples)
        print("częstotliwość ", freq)
        print("milisekundy", seconds * 1000)   
        print("czas między próbkami", sample_time)

        self.plot_input(channel)
        self.plot_spektogram(channel)
        

    def record(self):
        recording = sd.rec(self.frequency*self.seconds, samplerate=self.frequency, channels=2)
        sd.wait()
        wavfile.write("test11.wav", self.frequency, recording)
        self.plot("test11.wav")

    def play(self, file_name):
        freq, data = wavfile.read(file_name)
        sd.play(data,freq)




        


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Aplikacja")
    root.geometry("900x900")
    root.resizable(False,False)
    app = Aplikacja(root)
    root.mainloop()