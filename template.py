import sys,math,itertools,re,numpy,string

def int_line_input(): return map(int,input().split())
def int_list_input(n:int):
	li=[int_line_input() for _ in range(n)]
	return [[0]+list(i) for i in zip(*li)]
def int_grid_input(h:int,w:int,n:int):
	for _ in range(n): yield [[0]*(w+2)]+[[0]+list(map(int,input().split()))+[0] for _ in range(h)]+[[0]*(w+2)]
def str_grid_input(h:int,w:int,n:int,t:str):
	for _ in range(n): yield [t*(w+2)]+[t+input()+t for _ in range(h)]+[t*(w+2)]
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
		while(True):
			min_cost=math.inf
			for i in range(1,self.vertices+1):
				if not(self.status[i]) and result[i]<=min_cost:
					view=i
					min_cost=result[i]
			self.status[view]=True
			for i in self.graph[view]:
				if not(self.status[i[0]]):
					result[i[0]]=min(result[view]+i[1],result[i[0]])
			if t is None:
				if not False in self.status[1:]:
					break
			else:
				if self.status[t]:
					break
		return(result)
