#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
#include <map>
using Mat=std::array<uint16_t,4>;struct State{Mat e{},o{};};struct Gate{std::array<int,4>p,n;};
uint16_t mt[16][65536];int mul[16][16],inv[16];std::vector<Gate> gates,thin;std::vector<int> prog;
uint64_t nodes[6]{},prune[6]{},hits=0;int mask=27;
int rank(Mat a){int r=0;for(int c=0;c<4;c++){int j=r;while(j<4&&!((a[j]>>(4*c))&15))j++;if(j==4)continue;std::swap(a[j],a[r]);a[r]=mt[inv[(a[r]>>(4*c))&15]][a[r]];for(j=r+1;j<4;j++){int q=(a[j]>>(4*c))&15;if(q)a[j]^=mt[q][a[r]];}if(++r==4)break;}return r;}
Mat inverse(Mat a){Mat b{};for(int i=0;i<4;i++)b[i]=1<<(4*i);for(int c=0;c<4;c++){int j=c;while(j<4&&!((a[j]>>(4*c))&15))j++;if(j==4)return{};std::swap(a[j],a[c]);std::swap(b[j],b[c]);int x=inv[(a[c]>>(4*c))&15];a[c]=mt[x][a[c]];b[c]=mt[x][b[c]];for(j=0;j<4;j++)if(j!=c){int q=(a[j]>>(4*c))&15;a[j]^=mt[q][a[c]];b[j]^=mt[q][b[c]];}}return b;}
std::array<uint16_t,16> sums(Mat a){std::array<uint16_t,16>s{};for(int i=1;i<16;i++)s[i]=s[i&(i-1)]^a[__builtin_ctz(i)];return s;}
State apply(State s,Gate g,int d){auto e=sums(s.e),o=sums(s.o);State t;for(int i=0;i<4;i++){t.e[i]=s.e[i]^mt[d^1][e[g.p[i]]]^mt[d][o[g.n[i]]];t.o[i]=s.o[i]^mt[d^1][o[g.p[i]]]^mt[d][e[g.n[i]]];}return t;}
std::array<int,4> lastN(State s){auto oi=inverse(s.o);if(oi==Mat{})return{};std::array<int,4>n{};for(int i=0;i<4;i++){uint16_t x=0;for(int k=0;k<4;k++)x^=mt[(s.e[i]>>(4*k))&15][oi[k]];for(int j=0;j<4;j++){int a=(x>>(4*j))&15;if(a>1)return{};n[i]|=a<<j;}}return n;}
void dfs(State s,int step){nodes[step]++;int rem=5-step;if(rem<4&&rank(s.e)>rem){prune[step]++;return;}if(step==4){auto n=lastN(s);if(n==std::array<int,4>{})return;const auto&v=(mask>>4&1)?gates:thin;for(int i=0;i<(int)v.size();i++)if(v[i].n==n){auto t=apply(s,v[i],(mask>>4&1)?6:1);if(t.e!=Mat{})continue;hits++;std::cout<<"HIT "<<mask;for(int j:prog)std::cout<<" "<<j;std::cout<<" "<<i<<"\n";}return;}
 const auto&v=(mask>>step&1)?gates:thin;int d=(mask>>step&1)?step+2:1;auto se=sums(s.e),so=sums(s.o);
 for(int i=0;i<(int)v.size();i++){auto&g=v[i];State t;for(int k=0;k<4;k++){t.e[k]=s.e[k]^mt[d^1][se[g.p[k]]]^mt[d][so[g.n[k]]];t.o[k]=s.o[k]^mt[d^1][so[g.p[k]]]^mt[d][se[g.n[k]]];}prog.push_back(i);dfs(t,step+1);prog.pop_back();}
}
int main(int argc,char**argv){if(argc>1)mask=std::stoi(argv[1]);for(int a=0;a<16;a++)for(int b=0;b<16;b++){int v=0;for(int x=a,y=b;y;y>>=1){if(y&1)v^=x;x<<=1;if(x&16)x^=19;}mul[a][b]=v;}for(int a=1;a<16;a++)for(int b=1;b<16;b++)if(mul[a][b]==1)inv[a]=b;for(int d=0;d<16;d++)for(int x=0;x<65536;x++){int v=0;for(int k=0;k<4;k++)v|=mul[d][(x>>(4*k))&15]<<(4*k);mt[d][x]=v;}
 for(int u=1;u<16;u++)for(int v=1;v<16;v++)if(!(__builtin_popcount(u&v)&1)){
  Gate g{};for(int i=0;i<4;i++)if(u>>i&1)g.n[i]=v;thin.push_back(g);
  std::map<std::array<int,4>,bool>seen;
  for(int a=1;a<16;a++)if(__builtin_popcount(v&a)&1)for(int b=1;b<16;b++)if((__builtin_popcount(u&b)&1)&&!(__builtin_popcount(a&b)&1)){
   for(int i=0;i<4;i++)g.p[i]=((u>>i&1)?b:0)^((a>>i&1)?v:0);
   if(!seen[g.p]){seen[g.p]=true;gates.push_back(g);}}
 }
 std::cerr<<"full="<<gates.size()<<" thin="<<thin.size()<<"\n";State s;for(int i=0;i<4;i++)s.e[i]=1<<(4*i);
 auto&v=(mask&1)?gates:thin;for(int i=0;i<(int)v.size();i++)if(v[i].n==std::array<int,4>{0,1,0,0}&&(!(mask&1)||v[i].p==std::array<int,4>{1,2,0,0})){prog.push_back(i);dfs(apply(s,v[i],(mask&1)?2:1),1);break;}
 std::cerr<<"mask="<<mask<<" hits="<<hits;for(int i=0;i<5;i++)std::cerr<<" s"<<i<<"="<<nodes[i]<<"/"<<prune[i];std::cerr<<"\n";
}
