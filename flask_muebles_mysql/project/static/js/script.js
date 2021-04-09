function validarCamposLetras(valor){
    const WHITE_LIST_MAY = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
    const WHITE_LIST_MIN = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z"];
    const WHITE_LIST_NUM = [".","0","1","2","3","4","5","6","7","8","9","0","-"," ","@","_"];
    const WHITE_LIST_EXC = ["Á","É","Í","Ó","Ú","á","é","í","ó","ú"];

    str = '';

    if(valor.length > 0){
        for(let i of valor){
            str += WHITE_LIST_MAY.indexOf(i) > -1 ? i : '';
            str += WHITE_LIST_MIN.indexOf(i) > -1 ? i : '';
            str += WHITE_LIST_NUM.indexOf(i) > -1 ? i : '';
            str += WHITE_LIST_EXC.indexOf(i) > -1 ? i : '';
        }
    }else
        str = '0';

    return str;
}