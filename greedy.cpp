// Chu Thien Hai 20215360
#include<bits/stdc++.h>
using namespace std;

int N;
const int NMAX = 1e3 + 5;
int e[NMAX], l[NMAX], d[NMAX];
int c[NMAX][NMAX];
int cd[NMAX][NMAX];
int route[NMAX];
int timeCome[NMAX];

vector<int> orderToCome;
vector<pair<int,int>> orderByL;

void input() {
    cin >> N;
    for (int i = 1; i <= N; i++) {
        cin >> e[i] >> l[i] >> d[i];
        orderByL.push_back({l[i],i});
    }
    for (int i = 0; i <= N; i++) {
        for (int j = 0; j <= N; j++) {
            cin >> c[i][j];
            cd[i][j] = c[i][j] + d[j];
        }
    }
}

void changeOrderToCome(int high, int low, int oldOrder[]){
    int tmp = oldOrder[high];
    for (int i = high; i > low; i--){
        oldOrder[i] = oldOrder[i-1];
    }
    oldOrder[low] = tmp;
}

int main() {
    input();
    int orderToCome[NMAX];
    sort(orderByL.begin(), orderByL.end());
    for (int i = 1; i <= N; i++){
        orderToCome[i] = orderByL[i-1].second;
    }
    route[0] = 0;
    timeCome[0] = 0;
    for (int i = 1; i <= N; i++){

        int nextLocation = orderToCome[i];
        int selectedLocation = nextLocation;
        int lastestTimeCome = l[selectedLocation];
        int selectedTimeCome = max(e[selectedLocation], timeCome[route[i-1]] + cd[route[i-1]][selectedLocation]);
        int tmp_j;
        for (int j = i + 1; j <= N; j++){
          int choice = orderToCome[j];
                // Gia su den diem choice truoc, roi moi di den nextLocation
                // (van thoa man dieu kien co the den truoc thoi diem l[nextLocation])
                // ==> Tim ra diem den tiep theo co timeCome nho nhat
          int tmpTimeCome = max(e[choice], timeCome[route[i-1]] + cd[route[i-1]][choice]);
          if(tmpTimeCome + cd[choice][selectedLocation] < lastestTimeCome){
                lastestTimeCome = tmpTimeCome + cd[choice][selectedLocation];
                selectedLocation = choice;
                selectedTimeCome = tmpTimeCome;
                tmp_j = j;
                }
        }
        if (selectedLocation != nextLocation){
            changeOrderToCome(tmp_j, i, orderToCome);
        }
        route[i] = selectedLocation;
        timeCome[route[i]] = selectedTimeCome;
    }

    cout << N << endl;
    for (int i = 1; i <= N; i++) {
        cout << route[i] << " ";
    }
    return 0;
}
