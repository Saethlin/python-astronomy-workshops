from custom import *

if not os.path.exists('rings removed'):
    os.mkdir('rings removed')
os.chdir('reduced')

previous = []

files = os.listdir('.')
for f in files:
    print(f)
    start_time = now()
    img = readfits(f)
    for i in (1,0):
        im = img[i]
        
        if i == 0:
            x,y = radialbin(im,-1400+976*2,-375+(-10)*2)
        else:
            x,y = radialbin(im,-2650+976*2,-1525+(-10)*2)
        
        y[0] = y[1]
        
        smoothed = csmooth(y,100)
        
        ifunc = interp1d(x,smoothed,kind='slinear')
        
        '''
        plt.plot(x,y,'kx')
        plt.plot(x,smoothed,'r-')
        os.chdir('..')
        plt.savefig(f[:-4]+'png',bbox_inches='tight')
        plt.clf()
        os.chdir('reduced')
        '''
        
        #Really no need at all for fitting if we can interpolate
        
        pos = np.mgrid[:im.shape[0],:im.shape[1]]
        if i == 0:
            pos[0] -= -1400+976*2
            pos[1] -= -375+(-10)*2
        else:
            pos[0] -= -2650+976*2
            pos[1] -= -1525+(-10)*2
        
        dst = np.sqrt(sum(pos**2,axis=0)).clip(x.min(),x.max())
        rings = ifunc(dst)
        rings[dst == dst.min()] = smoothed[0]
        
        img[i] = (im-rings).clip(0)
    
    lines = imhead(f)[6:9]
    
    img = np.hstack((img[0],img[1]))
    
    os.chdir('..\\rings removed')
    writefits(img,f[:-4]+'nr.fits',lines)
    os.chdir('..\\reduced')
    
    print(now()-start_time)