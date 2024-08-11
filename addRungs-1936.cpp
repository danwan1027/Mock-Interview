class Solution {
public:
    int addRungs(vector<int>& rungs, int dist) {
        int a = 0, ans = 0;
        for(int i = 0 ; i < rungs.size() ; i++){
            if((rungs[i] - a) % dist == 0){
                ans = ans + (rungs[i] - a)/dist - 1;
            }
            else{
                ans = ans + (rungs[i] - a)/dist;
            }
            a = rungs[i];
        }
        return ans;
    }
};
