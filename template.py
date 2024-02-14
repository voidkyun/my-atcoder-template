import sys,math,itertools,re,numpy,string,heapq,collections,functools

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
		grid=StringGrid(h,w,[input() for _ in range(h)])
		return grid
	else:
		grid=StringGrid(h+2,w+2,[edge*(w+2)]+[edge+input()+edge for _ in range(h)]+[edge*(w+2)])
		return grid
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
def prime_factorize(n:int):
	result=[]
	cnt=0
	for i in range(2,int(pow(n,0.5)+1)):
		if n%i==0:
			result.append([i,0])
			cnt+=1
		while(n%i==0):
			n//=i
			result[cnt-1][1]+=1
	return result if n==1 else result+[[n,1]]

class UnweightedGraph:
	def __init__(self,vertices:int) -> None:
		self.vertices=vertices
		self.edges=0
		self.graph=[[] for _ in range(vertices+1)]
		self.status=[False for _ in range(vertices+1)]
	def add(self,u:int,v:int,directed=False):
		self.edges+=1
		self.graph[u].append(v)
		if not directed:
			self.graph[v].append(u)
	def generate_adjacency_matrix(self):
		self.adjacency_matrix=[[0 for _ in range(self.vertices+1)] for _ in range(self.vertices+1)]
		for i in range(1,self.vertices+1):
			for j in self.graph[i]:
				self.adjacency_matrix[i][j]+=1
	def bfs(self,s:int,initializestatus=False):
		if initializestatus:
			self.status=[False for _ in range(self.vertices+1)]
		queue=collections.deque()
		queue.append(s)
		self.status[s]=True
		result=[math.inf for _ in range(self.vertices+1)]
		result[s]=0
		self.passed=[]
		while(len(queue)>0):
			i=queue.pop()
			for j in self.graph[i]:
				if not self.status[j]:
					self.status[j]=True
					self.passed.append(j)
					result[j]=result[i]+1
					queue.appendleft(j)
		return result
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
	def find_hamiltonian_path(self,s:int):
		longpath=self.enumerate_long_paths(s)
		class hamiltonian_path():
			def __init__(self) -> None:
				self.cnt=0
				self.paths=[]
		result=hamiltonian_path()
		for i in range(longpath.cnt):
			if not False in longpath.status[i][1:]:
				result.cnt+=1
				result.paths.append(longpath.paths[i])
		return(result if result.cnt>0 else None)
	def exist_eulerian_path(self):
		cnt=0
		start=[]
		for i in range(1,self.vertices+1):
			if len(self.graph[i])%2==1:
				start.append(i)
				cnt+=1
		return [True,start] if cnt==2 or cnt==0 else [False,None]
	def find_eulerian_path(self):
		exist_eulerian_path=self.exist_eulerian_path()
		if exist_eulerian_path[0]:
			self.generate_adjacency_matrix()
			if len(exist_eulerian_path[1])>0:
				start=exist_eulerian_path[1][0]
			else:
				start=1
			path=collections.deque()
			def search(self:UnweightedGraph,u:int,path:collections.deque):
				for v in range(1,self.vertices+1):
					if self.adjacency_matrix[u][v]>0:
						self.adjacency_matrix[u][v]-=1
						if self.adjacency_matrix[v][u]>0:
							self.adjacency_matrix[v][u]-=1
						search(self,v,path)
				path.appendleft(u)
			search(self,start,path)
			return list(path)
		else:
			return None
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
		self.edgelist=[]
		self.status=[False for _ in range(self.vertices+1)]
	def add(self,u:int,v:int,w:int,directed=False):
		self.edges+=1
		self.edgelist.append([u,v,w,directed])
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
	def bellmanford(self,s:int):
		result=[math.inf for _ in range(self.vertices+1)]
		result[s]=0
		for _ in range(self.edges-1):
			for u,v,w,directed in self.edgelist:
				if not(directed):return(None)
				result[v]=min(result[v],result[u]+w)		
		for u,v,w,directed in self.edgelist:
			if result[u]+w<result[v]:
				return(None)
		else:
			return(result)
class StringGrid:
	def __init__(self,height:int,width:int,grid:list) -> None:
		self.grid=grid
		self.height=height
		self.width=width
		self.status=[[False for _ in range(self.width)] for _ in range(self.height)]
		self.ismaze=False
	def mazeify(self,pathchar:str,wallchar:str):
		self.pathchar=pathchar
		self.wallchar=wallchar
		self.ismaze=True
	def bfs(self,si:int,sj:int,initializestatus=False):
		if initializestatus:
			self.status=[[False for _ in range(self.width)] for _ in range(self.height)]
		queue=collections.deque()
		queue.append([si,sj])
		self.status[si][sj]=True
		result=[[math.inf for _ in range(self.width+2)] for _ in range(self.height+2)]
		result[si][sj]=0
		while(len(queue)>0):
			i,j=queue.pop()
			if not(self.status[i-1][j]) and self.grid[i-1][j] in self.pathchar:
				self.status[i-1][j]=True
				result[i-1][j]=result[i][j]+1
				queue.appendleft([i-1,j])
			if not(self.status[i][j+1]) and self.grid[i][j+1] in self.pathchar:
				self.status[i][j+1]=True
				result[i][j+1]=result[i][j]+1
				queue.appendleft([i,j+1])
			if not(self.status[i+1][j]) and self.grid[i+1][j] in self.pathchar:
				self.status[i+1][j]=True
				result[i+1][j]=result[i][j]+1
				queue.appendleft([i+1,j])
			if not(self.status[i][j-1]) and self.grid[i][j-1] in self.pathchar:
				self.status[i][j-1]=True
				result[i][j-1]=result[i][j]+1
				queue.appendleft([i,j-1])
		return result
	def dfs(self,i:int,j:int,initializestatus=False,isfirst=True):
		if initializestatus:
			self.status=[[False for _ in range(self.width)] for _ in range(self.height)]
		if isfirst:
			self.passed=[]
		if not(self.status[i][j]) and self.grid[i][j] in self.pathchar:
			self.status[i][j]=True
			self.passed.append([i,j])
			self.dfs(i-1,j,False,False)
			self.dfs(i,j+1,False,False)
			self.dfs(i+1,j,False,False)
			self.dfs(i,j-1,False,False)

