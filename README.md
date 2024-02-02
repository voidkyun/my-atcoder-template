# my-atcoder-template

## function
### int_line_input‎
1行の空白区切りの整数を入力　例：`0 1 2 3`
### int_list_input‎
縦並びの複数の配列を入力
<br>例：
```
a1 b1 c1
a1 b2 c2
a3 b3 c3
```
### int_grid_input
整数のグリッドを入力
<br>例：
```
a(1,1) a(1,2) a(1,3)
a(2,1) a(2,2) a(2,3)
```
### str_grid_input
文字列のグリッドを入力
StringGridクラスを返す
<br>例：
```
a(1,1)...a(1,w)
.
.
a(h,1)...a(h,w)
```
### unweighted_graph_input
重み無しグラフを入力
UnweightedGraphクラスを返す
### weighted_graph_input
重み付きグラフを入力
WeightedGraphクラスを返す
### gcd
2つの整数の最大公約数を求める
### prime_factorize
整数を素因数分解する
<br>返値：
```
n=12のとき　[[2,2],[3,1]]
```
## UnweightedGraph
### method
- add グラフに辺を追加
- bfs　特定の頂点から幅優先探索を行う。各頂点への最短経路のリストを返す。UnweightedGraph.statusに結果を代入する。
- dfs　特定の頂点から深さ優先探索を行う。UnweightedGraph.statusに結果を代入する。UnweightedGraph.passedには通った順に頂点の番号が代入される。
- enumerate_long_paths‎　特定の頂点から始まり、これ以上進めなくなった頂点で終了するパスを列挙する
- connected_components　グラフの連結成分を列挙する
- connected　グラフが連結かどうかをboolで返す
- ispathgraph　グラフがパスグラフであるかどうかをboolで返す
## WeightedGraph
### method
- add グラフに辺を追加
- dijkstra ダイクストラ法を用いて最短経路を求める。
## StringGrid
### method
- mazeify　グリッドを迷路として定義する。塀となる文字列と道となる文字列を指定する。
- bfs　特定のマスから幅優先探索を行う。各マスへの最短経路のリストを返す。StringGrid.statusに結果を代入する。
- dfs　特定のマスから深さ優先探索を行う。StringGrid.statusに結果を代入する。StringGrid.passedには通った順に頂点の番号が代入される。
