Q='index.html'
import os,sys,unicodedata as D
from pathlib import Path as A
from datetime import datetime as Z
a={'.git','.github',Q,'.nojekyll'}
def C(text):
	A=0
	for B in text:
		if D.east_asian_width(B)in('F','W'):A+=2
		else:A+=1
	return A
def b(name,max_width):
	F=max_width;D=name;J=C(D)
	if J<=F:return D
	E=F-3;A='';B=0;G=0
	for(K,H)in enumerate(D):
		I=C(H)
		if B+I>E:break
		A+=H;B+=I;G=K
	if B+2>E:
		while B+2>E and A:L=A[-1];A=A[:-1];B-=C(L);G-=1
	return A+'..'+'>'
def P(directory,base_dir):
	Y='utf-8';X='original_name';W='display_width';V='size';U='path';T='/files/';O='is_dir';N='date';M='name';J=base_dir;I='/';D=directory;R=D/Q
	if D==J:E=T
	else:E=T+str(D.relative_to(J)).replace('\\',I)+I
	B=[]
	for A in D.iterdir():
		if A.name in a:continue
		c=Z.fromtimestamp(A.stat().st_mtime);d=c.strftime('%d-%b-%Y %H:%M');K=A.is_dir();H=A.name+I if K else A.name;e='-'if K else str(A.stat().st_size);B.append({M:H,U:H,N:d,V:e,O:K,W:C(H),X:H})
	if not B:
		F=f'''<html>
<head><title>Index of {E}</title></head>
<body>
<h1>Index of {E}</h1><hr><pre><a href="../">../</a>
</pre><hr></body>
</html>'''
		with open(R,'w',encoding=Y)as L:L.write(F)
		return
	B.sort(key=lambda x:(not x[O],x[M].lower()));G=max(A[W]for A in B)if B else 0;G=min(G,50);F=f'<html>\n<head><title>Index of {E}</title></head>\n<body>\n<h1>Index of {E}</h1><hr><pre><a href="../">../</a>\n'
	for A in B:S=b(A[X],G);f=C(S);g=' '*(G-f+50-G);h=' '*(20-len(A[N]));F+=f'<a href="{A[U]}">{S}</a>{g}{A[N]}{h}{A[V]}\n'
	F+='</pre><hr></body>\n</html>'
	with open(R,'w',encoding=Y)as L:L.write(F)
	for A in B:
		if A[O]:P(D/A[M].rstrip(I),J)
if __name__=='__main__':B=A(sys.argv[1])if len(sys.argv)>1 else A('.');E=B;P(B,E)
