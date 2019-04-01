

from matplotlib.pyplot import text
import matplotlib.pyplot as plt
import platform

pf = '/'
if platform.system() == 'Windows':
    pf= '\\'

def plot_matrix_file(path,op,csvf,plots, f):
    file = open(path+pf+op+pf+csvf+pf+f, 'r')
    file.readline()
    x = [x for x in range(0,15)]
    for line in file:
        line = line.split(',')
        nn = line[0]
        y = list(map(int, line[1:-1]))
        y = [0,0]+y
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        plt.plot(x,y)
        plt.xlim(2, 16)   
        ymax = max(y)
        xpos = y.index(ymax)
        xmax = x[xpos]
        ax.annotate('local max', xy=(xmax, ymax), xytext=(xmax, ymax+8),
                    arrowprops=dict(facecolor='black', shrink=0.05),)
        ax.set_ylim(100,220) 
        plt.ylabel('No. of cavities correctly predicited for proteins ')
        plt.xlabel('Burriedness')
        plt.title(nn)
        plt.savefig(path+pf+op+pf+plots+pf+nn+'.png')
        plt.grid(True)
        text(xpos+2, ymax+7, (xpos, ymax), fontsize=12)
        plt.show()
        plt.close()    
    file.close()
    print("Plots are created") 

