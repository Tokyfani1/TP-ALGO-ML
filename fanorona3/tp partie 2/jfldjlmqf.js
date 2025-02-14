
function isAlignedX(x){
    var compt = 0;

    for(var i=0;i<3;i++){
        for(var j=0;j<3;j++){
            if(arrayPosition[i][j] == x){
                compt++;
            }
        }
        if(compt == 3){
            return true;
        }
        compt = 0;
    }

    return false;
}

function isAlignedY(x){
    var compt = 0;

    for(var i=0;i<3;i++){
        for(var j=0;j<3;j++){
            if(arrayPosition[j][i] == x){
                compt++;
            }
        }
        if(compt == 3){
            return true;
        }
        compt = 0;
    }

    return false;
}

function isAlignedDiag(x){
    if(x == arrayPosition[0][0] || x == arrayPosition[2][2] || x == arrayPosition[1][1])
        if(arrayPosition[1][1] == arrayPosition[0][0] && arrayPosition[1][1] == arrayPosition[2][2])
            return true;
    
    if(x == arrayPosition[0][2] || x == arrayPosition[2][0] || x == arrayPosition[1][1])
        if(arrayPosition[1][1] == arrayPosition[0][2] && arrayPosition[1][1] == arrayPosition[2][0])
            return true;

    return false;
}
