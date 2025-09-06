_A='index.html'
import os,sys,unicodedata
from pathlib import Path
from datetime import datetime
ignore_list={'.git','.github',_A,'.nojekyll'}
def get_east_asian_width_count(text):
        A=0
        for B in text:
                if unicodedata.east_asian_width(B)in('F','W'):A+=2
                else:A+=1
        return A
def format_filename(name,max_width):
        E=max_width;C=name;I=get_east_asian_width_count(C)
        if I<=E:return C
        D=E-3;A='';B=0;F=0
        for(J,G)in enumerate(C):
                H=get_east_asian_width_count(G)
                if B+H>D:break
                A+=G;B+=H;F=J
        if B+2>D:
                while B+2>D and A:K=A[-1];A=A[:-1];B-=get_east_asian_width_count(K);F-=1
        return A+'..'+'>'
def generate_index(directory,base_dir):
        U='utf-8';T='original_name';S='display_width';R='size';Q='path';N='is_dir';M='date';L='name';I=base_dir;D=directory;C='/';O=D/_A
        if D==I:E=C
        else:E=C+str(D.relative_to(I)).replace('\\',C)+C
        B=[]
        for A in D.iterdir():
                if A.name in ignore_list:continue
                V=datetime.fromtimestamp(A.stat().st_mtime);W=V.strftime('%d-%b-%Y %H:%M');J=A.is_dir();H=A.name+C if J else A.name;X='-'if J else str(A.stat().st_size);B.append({L:H,Q:H,M:W,R:X,N:J,S:get_east_asian_width_count(H),T:H})
        if not B:
                F=f'''<html>
<head><title>Index of {E}</title></head>
<body>
<h1>Index of {E}</h1><hr><pre><a href="../">../</a>
</pre><hr></body>
</html>'''
                with open(O,'w',encoding=U)as K:K.write(F)
                return
        B.sort(key=lambda x:(not x[N],x[L].lower()));G=max(A[S]for A in B)if B else 0;G=min(G,50);F=f'<html>\n<head><title>Index of {E}</title></head>\n<body>\n<h1>Index of {E}</h1><hr><pre><a href="../">../</a>\n'
        for A in B:P=format_filename(A[T],G);Y=get_east_asian_width_count(P);Z=' '*(G-Y+50-G);a=' '*(20-len(A[M]));F+=f'<a href="{A[Q]}">{P}</a>{Z}{A[M]}{a}{A[R]}\n'
        F+='</pre><hr></body>\n</html>'
        with open(O,'w',encoding=U)as K:K.write(F)
        for A in B:
                if A[N]:generate_index(D/A[L].rstrip(C),I)
if __name__=='__main__':target_dir=Path(sys.argv[1])if len(sys.argv)>1 else Path('.');base_dir=target_dir;generate_index(target_dir,base_dir)
