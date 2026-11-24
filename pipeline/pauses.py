import subprocess,numpy as np,sys
def pauses(fn, thr=None, minlen=0.2):
    a=subprocess.run(['ffmpeg','-v','error','-i',fn,'-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout
    x=np.frombuffer(a,np.int16).astype(float); w=400
    e=np.array([20*np.log10(np.sqrt(np.mean(x[i:i+w]**2))+1) for i in range(0,len(x)-w,w)])
    thr=thr or (np.median(e)-12)
    low=e<thr; out=[]; i=0
    while i<len(low):
        if low[i]:
            j=i
            while j<len(low) and low[j]: j+=1
            if (j-i)*0.05>=minlen: out.append((round(i*0.05,2),round(j*0.05,2)))
            i=j
        else: i+=1
    return out, len(e)*0.05
if __name__=='__main__':
    for f in sys.argv[1:]:
        p,d=pauses(f); print(f, round(d,1), p)
