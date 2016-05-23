from custom import *

data = np.load('norings-save.npz')

standards = data['standards']
target = data['target']
airmass = data['airmass']
exptime = data['exptime']
time = data['opentime']
error = data['error']
target_centroid = data['target_centroid']
standard_centroid = data['standard_centroid']
coords = data['coords']
obj = data['obj']

ingress = 2455211.517
egress = 2455211.569

in_mask = (time > ingress) & (time < egress)
out_mask = np.invert(in_mask)

#Remove any standards with flux less than 0
good = np.ones(standards.shape[0],bool)
for i in range(standards.shape[0]):
    if np.any(standards[i] < 0):
        good[i] = False

standards = standards[good]
coords = coords[good]


#Normalize everything
target /= np.median(target)
for i in range(standards.shape[0]):
    standards[i] /= median(standards[i])

standards /= np.median(standards, axis=1)[:, np.newaxis]


#Remove standards one by one by standard deviation until only three left
#Sort the normed standards by the out-of-occultation standard deviation
norm = np.zeros(standards.shape)
for i in range(standards.shape[0]):
    norm[i] = target/standards[i]


stdev = np.zeros(norm.shape[0])
for i in range(standards.shape[0]):
    stdev[i] = mad(norm[i])
#stdev = std(norm[:,out_mask],axis=1)
standards = standards[np.argsort(stdev)]
coords = coords[np.argsort(stdev)]


#Remove any standards that are within the sky radius of another standard
#We have sorted the standards by standard deviation, so we prefer the
#instance that comes first
mask = np.ones(standards.shape[0],bool)
for i in range(standards.shape[0]):
    if mask[i]:
        j = i+1
        while j < coords.shape[0] and np.sqrt((coords[j,0]-coords[i,0])**2+(coords[j,1]-coords[i,1])**2) < 2*obj:
            mask[j] = False
            j += 1

#Remove the standards that are too close together
standards = standards[mask]
coords = coords[mask]
standards = standards[1:]

nstars = np.zeros(standards.shape[0]-3)
stdev = np.zeros(standards.shape[0]-3)


f = standards.copy()
i = 0
while f.shape[0] > 3:
    f = f[:-1]
    s = sum(f,0)
    test = target/s
    test /= np.median(test)
    
    nstars[i] = f.shape[0]
    stdev[i] = mad(test)
    
    i += 1
print('Standards used:',nstars[np.argmin(stdev)])

#Process data using number of standards determined
standards = standards[:nstars[np.argmin(stdev)]]
np.save('smcoords.npy',coords[:nstars[np.argmin(stdev)]])
s = sum(standards,0)
flux = target/s
flux /= np.median(flux)

for i in range(standards.shape[0]):
    test = target/standards[i]
    #test = standards[i]
    test /= np.median(test)
    plt.plot(time,test,'ko')
    plt.plot(time,test,'b-')
    
    plt.plot([egress,egress],[0,2],'r-')
    plt.plot([ingress,ingress],[0,2],'r-')
    
    plt.axis([time[0],time[-1],0.98,1.02])
    #plt.show()
    fig = plt.gcf()
    fig.set_size_inches(14,8)
    plt.savefig(str(i)+'.png')
    plt.clf()

'''
lbound = np.median(flux)-3*mad(flux)
ubound = np.median(flux)+3*mad(flux)
mask = (flux > lbound) & (flux < ubound)
flux = flux[mask]
time = time[mask]
out_mask = out_mask[mask]
in_mask = in_mask[mask]
error = error[mask]
airmass = airmass[mask]
target_centroid = target_centroid[mask]
'''

'''
Detrending
'''
for parm in [airmass,target_centroid[:,0],target_centroid[:,1]]:
    p = np.polyfit(parm,flux,1)
    #plt.plot(parm,flux,'ko')
    #plt.plot(parm,np.polyval(p,parm))
    #plt.show()
    flux /= np.polyval(p,parm)


flux /= np.median(flux[out_mask])


ofil = open('Flux stats.txt','w')
weights = 1/(error**2)

mean_out = np.average(flux[out_mask],weights=weights[out_mask])
sigma_out = np.std(flux[out_mask])/np.sqrt(sum(out_mask))

mean_in = np.average(flux[in_mask],weights=weights[in_mask])
sigma_in = np.std(flux[in_mask])/np.sqrt(sum(in_mask))

sig = (mean_out-mean_in)/(sigma_in+sigma_out)

ofil.write('Mean out\t'+str(mean_out)+'\t'+str(sigma_out)+'\n')
ofil.write('Mean in\t'+str(mean_in)+'\t'+str(sigma_in)+'\n')
ofil.write('Significance\t'+str(sig)+'\n')

med_out = np.median(flux[out_mask])
mad_out = mad(flux[out_mask])/np.sqrt(sum(out_mask))

med_in = np.median(flux[in_mask])
mad_in = mad(flux[in_mask])/np.sqrt(sum(in_mask))

sig = (med_out-med_in)/(mad_in+mad_out)

ofil.write('Median out\t'+str(med_out)+'\t'+str(mad_out)+'\n')
ofil.write('Median in\t'+str(med_in)+'\t'+str(mad_in)+'\n')
ofil.write('Significance\t'+str(sig)+'\n')

ofil.close()

plt.hist(flux[in_mask], 10, facecolor='g', alpha=0.5)
plt.hist(flux[out_mask],10,facecolor='b',alpha=0.5)
plt.clf()

'''
Test for red noise by binning up the data and checking if it matches poisson
'''

'''
s = 10
bsize = np.arange(s)+1
bstdev = np.zeros(s)
bstdev[0] = std(flux)
for i in range(2,s+1):
    bstdev[i-1] = std(binup(flux[out_mask],i))

poisson = 1/np.sqrt(bsize)
poisson /= poisson[0]/bstdev[0]

beta = bstdev[-1]/(poisson[-1]/np.sqrt(bsize[-1]))
print('Beta:',beta)

plt.title('Red Noise Test')
plt.xlabel('Bin Size')
plt.ylabel('Standard Deviation')
plt.plot(bsize,bstdev,'ko')
plt.plot(bsize,poisson,'r-')
fig = plt.gcf()
fig.set_size_inches(14,8)
plt.savefig('RedNoise.png')
plt.clf()
'''

mid = (ingress+egress)/2
time -= mid
ingress -= mid
egress -= mid

#error *= beta
tdelta = time[1]-time[0]
plt.title('CoRoT-7 UT2010-01-15 GTC OSIRIS')
plt.xlabel('Time to Mid-Occultation (d)')
plt.ylabel('Relative Flux')
plt.plot([egress,egress],[0,2],'r-')
plt.plot([ingress,ingress],[0,2],'r-')
plt.errorbar(time,flux,yerr=error,fmt='bo')
plt.axis([time[0]-tdelta,time[-1]+tdelta,0.98,1.02])
fig = plt.gcf()
fig.set_size_inches(14,8)
plt.savefig('CoRoT-7.png')
plt.clf()

np.savez('flux.npz',time=time,flux=flux,error=error)