/*********************************************
 * OPL 12.6.0.0 Model
 * Author: Fatih
 * Creation Date: 26 Haz 2021 at 20:58:33
 *********************************************/

range nodes = 1..5;
range facilities = 1..5;

int dist[nodes][nodes] =...;
int flow[facilities][facilities] =...;

dvar boolean assign[i in nodes][j in nodes][k in nodes][l in nodes];
dvar boolean test[i in nodes][j in nodes];

minimize sum(i,j,k,l in nodes) assign[i][j][k][l]*dist[j][l]*flow[i][k];

subject to{

forall(i in nodes) sum(j,k,l in nodes : i != k) assign[i][j][k][l] == 4;
forall(k in nodes) sum(i,j,l in nodes : i != k) assign[i][j][k][l] == 4;
forall(j in nodes) sum(i,k,l in nodes : j != l) assign[i][j][k][l] == 4;
forall(l in nodes) sum(i,j,k in nodes : j != l) assign[i][j][k][l] == 4;

forall(i,j,k,l in nodes : i == k ) assign[i][j][k][l] == 0;
forall(i,j,k,l in nodes : j == l ) assign[i][j][k][l] == 0;

forall(i,j in nodes) sum(k,l in nodes) assign[i][j][k][l] == sum(k2,l2 in nodes) assign[k2][l2][i][j];

forall(i,j in nodes) sum(k,l in nodes) assign[i][j][k][l] >= test[i][j];
forall(i,j in nodes) test[i][j] * 9999999 >= sum(k,l in nodes) assign[i][j][k][l];

forall(i in nodes) sum(j in nodes) test[i][j] == 1;

}

