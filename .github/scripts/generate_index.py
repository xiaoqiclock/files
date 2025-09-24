Q='index.html'
import os,sys,unicodedata as C
from pathlib import Path as A
from datetime import datetime as Y
Z={'.git','.github',Q,'.nojekyll','404.html','50x.html'}
def D(text):
	A=0
	for B in text:
		if C.east_asian_width(B)in('F','W'):A+=2
		else:A+=1
	return A
def a(name,max_width):
	F=max_width;C=name;J=D(C)
	if J<=F:return C
	E=F-3;A='';B=0;G=0
	for(K,H)in enumerate(C):
		I=D(H)
		if B+I>E:break
		A+=H;B+=I;G=K
	if B+2>E:
		while B+2>E and A:L=A[-1];A=A[:-1];B-=D(L);G-=1
	return A+'..'+'>'
def P(directory,base_dir):
	X='utf-8';W='original_name';V='display_width';U='size';T='path';O='is_dir';N='date';M='name';J=base_dir;E=directory;C='/';R=E/Q
	if E==J:F=C
	else:F=C+str(E.relative_to(J)).replace('\\',C)+C
	B=[]
	for A in E.iterdir():
		if A.name in Z:continue
		b=Y.fromtimestamp(A.stat().st_mtime);c=b.strftime('%d-%b-%Y %H:%M');K=A.is_dir();I=A.name+C if K else A.name;d='-'if K else str(A.stat().st_size);B.append({M:I,T:I,N:c,U:d,O:K,V:D(I),W:I})
	if not B:
		G=f'''<html>
<head><title>Index of {F}</title></head>
<body>
<h1>Index of {F}</h1><hr><pre><a href="../">../</a>
</pre><hr></body>
</html>'''
		with open(R,'w',encoding=X)as L:L.write(G)
		return
	B.sort(key=lambda x:(not x[O],x[M].lower()));H=max(A[V]for A in B)if B else 0;H=min(H,50);G=f'<html>\n<head><title>Index of {F}</title></head>\n<body>\n<h1>Index of {F}</h1><hr><pre><a href="../">../</a>\n'
	for A in B:S=a(A[W],H);e=D(S);f=' '*(H-e+50-H);g=' '*(20-len(A[N]));G+=f'<a href="{A[T]}">{S}</a>{f}{A[N]}{g}{A[U]}\n'
	G+='</pre><hr></body>\n</html>'
	with open(R,'w',encoding=X)as L:L.write(G)
	for A in B:
		if A[O]:P(E/A[M].rstrip(C),J)
if __name__=='__main__':B=A(sys.argv[1])if len(sys.argv)>1 else A('.');E=B;P(B,E)
