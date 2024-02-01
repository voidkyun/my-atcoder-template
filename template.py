import sys,math,itertools,re,numpy,string,heapq,collections

sys.setrecursionlimit(10**9)

def int_line_input(): return map(int,input().split())
def int_list_input(n:int):
	li=[int_line_input() for _ in range(n)]
	return [[0]+list(i) for i in zip(*li)]
def int_grid_input(h:int,w:int,edge=None):
	if edge is None:
		return [list(map(int,input().split())) for _ in range(h)]
	else:
		return [[edge]*(w+2)]+[[edge]+list(map(int,input().split()))+[edge] for _ in range(h)]+[[edge]*(w+2)]
def str_grid_input(h:int,w:int,edge=None):
	if edge is None:
		return [input() for _ in range(h)]
	else:
		return [edge*(w+2)]+[edge+input()+edge for _ in range(h)]+[edge*(w+2)]
def unweighted_graph_input(n,m,directed=False):
	g=UnweightedGraph(n)
	for _ in range(m):
		g.add(*int_line_input(),directed)
	return(g)
def weighted_graph_input(n,m,directed=False):
	g=WeightedGraph(n)
	for _ in range(m):
		g.add(*int_line_input(),directed)
	return g

def gcd(a:int,b:int):
	if b==0:
		return a
	else:
		return gcd(b,a%b)

class UnweightedGraph:
	def __init__(self,vertices:int) -> None:
		self.vertices=vertices
		self.edges=0
		self.graph=[[] for _ in range(vertices+1)]
		self.status=[False for _ in range(vertices+1)]
	def add(self,u:int,v:int,directed=False):
		self.edges+=1
		self.graph[u].append(v)
		if not directed: self.graph[v].append(u)
	def dfs(self,n:int,initializestatus=False,isfirst=True):
		if initializestatus:
			self.status=[False for _ in range(self.vertices+1)]
		if isfirst:
			self.passed=[]
		if not self.status[n]:
			self.status[n]=True
			self.passed.append(n)
			for i in self.graph[n]:
				self.dfs(i,False,False)
	def enumerate_long_paths(self,s:int):
		status=[False for _ in range(self.vertices+1)]
		path=collections.deque()
		path.append(s)
		status[s]=True
		class long_paths_result:
			def __init__(self) -> None:
				self.cnt=0
				self.paths=[]
				self.status=[]
		result=long_paths_result()
		def search(self:UnweightedGraph,n:int,status,path,result:long_paths_result):
			para=False
			for i in self.graph[n]:
				if not status[i]:
					para=True
					status[i]=True
					path.append(i)
					search(self,i,status,path,result)
					status[i]=False
					path.pop()
			if not para:
				result.cnt+=1
				result.paths.append(list(path))
				result.status.append(status.copy())
		search(self,s,status,path,result)
		return result
	def connected_components(self):
		components=[]
		for i in range(1,self.vertices+1):
			if i==1:
				self.dfs(i,True)
				components.append(self.passed)
			if not self.status[i]:
				self.dfs(i)
				components.append(self.passed)
		return components
	def connected(self):
		self.dfs(1,True)
		return not(False in self.status[1:])
	def ispathgraph(self):
		for i in range(1,self.vertices+1):
			if len(self.graph[i])>2:
				degree_para=False
				break
		else:
			degree_para=True
		return(self.edges==self.vertices-1 and degree_para and self.connected())
class WeightedGraph:
	def __init__(self,vertices:int) -> None:
		self.vertices=vertices
		self.edges=0
		self.graph=[[] for _ in range(vertices+1)]
		self.status=[False for _ in range(self.vertices+1)]
	def add(self,u:int,v:int,w:int,directed=False):
		self.edges+=1
		self.graph[u].append([v,w])
		if not directed: self.graph[v].append([u,w])
	def dijkstra(self,s:int,t=None):
		result=[math.inf for _ in range(self.vertices+1)]
		result[s]=0
		queue=[]
		heapq.heapify(queue)
		heapq.heappush(queue,(0,1))
		while(len(queue)>0):
			cost,view=heapq.heappop(queue)
			self.status[view]=True
			for i,w in self.graph[view]:
				if not(self.status[i]) and cost+w<result[i]:
					result[i]=cost+w
					heapq.heappush(queue,(cost+w,i))
			if t is not None:
				if self.status[t]:
					break
		return(result)

