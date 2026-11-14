// DIMACS generator: 2-color [S,N], orders per class, AP middle-extremal, v>lam*u => u before v
#include <stdio.h>
#include <stdlib.h>
int S,N; double lam; int *ov; int nv=0; int TRUEV;
#define IDX(u,v) ((long)(u)*(N+1)+(v))
int col(int u){return u-S+1;}
int O(int u,int v){ if(u>v) return -O(v,u); if((double)v>lam*u) return TRUEV; long k=IDX(u,v); if(!ov[k]) ov[k]=++nv; return ov[k]; }
FILE *out; long ncl=0;
int buf[16]; int bl;
void clause(){ // write buf skipping TRUE
  for(int i=0;i<bl;i++) if(buf[i]==TRUEV) return;
  for(int i=0;i<bl;i++) if(buf[i]!=-TRUEV) fprintf(out,"%d ",buf[i]); fprintf(out,"0\n"); ncl++; }
int main(int argc,char**argv){ S=atoi(argv[1]); N=atoi(argv[2]); lam=atof(argv[3]); char*fn=argv[4];
  ov=calloc((long)(N+1)*(N+1),sizeof(int)); nv=N-S+1; TRUEV=++nv;
  out=fopen("body.tmp","w");
  fprintf(out,"%d 0\n",TRUEV); ncl++;
  fprintf(out,"%d 0\n",col(S)); ncl++;
  for(int u=S;u<=N;u++) for(int v=u+1;v<=N;v++) for(int w=v+1;w<=N;w++){
    if(w>lam*u && v>lam*u && w>lam*v) continue;
    int a=O(u,v),b=O(v,w),c=O(w,u);
    for(int s=0;s<2;s++){ int sg=s?1:-1;
      bl=0; buf[bl++]=sg*col(u); buf[bl++]=sg*col(v); buf[bl++]=sg*col(w); buf[bl++]=-a; buf[bl++]=-b; buf[bl++]=-c; clause();
      bl=0; buf[bl++]=sg*col(u); buf[bl++]=sg*col(v); buf[bl++]=sg*col(w); buf[bl++]=a; buf[bl++]=b; buf[bl++]=c; clause(); } }
  for(int x=S;x<=N;x++) for(int y=x+1;2*y-x<=N;y++){ int z=2*y-x; int a=O(x,y), b=O(z,y);
    for(int s=0;s<2;s++){ int sg=s?1:-1;
      bl=0; buf[bl++]=sg*col(x); buf[bl++]=sg*col(y); buf[bl++]=sg*col(z); buf[bl++]=-a; buf[bl++]=b; clause();
      bl=0; buf[bl++]=sg*col(x); buf[bl++]=sg*col(y); buf[bl++]=sg*col(z); buf[bl++]=a; buf[bl++]=-b; clause(); } }
  fclose(out);
  FILE*f=fopen(fn,"w"); fprintf(f,"p cnf %d %ld\n",nv,ncl); fclose(f);
  char cmd[512]; sprintf(cmd,"cat body.tmp >> %s && rm body.tmp",fn); system(cmd);
  // write var map for pairs
  FILE*m=fopen("varmap.txt","w"); for(int u=S;u<=N;u++) for(int v=u+1;v<=N;v++) if(ov[IDX(u,v)]) fprintf(m,"%d %d %d\n",u,v,ov[IDX(u,v)]); fclose(m);
  fprintf(stderr,"vars %d clauses %ld\n",nv,ncl); }
