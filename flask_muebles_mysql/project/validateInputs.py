class validate:
    def sanitizarNombre(cadena):
        caracteres='!"#$%&\'()*+,-./0123456789:;=?@[\]^_`{|}~°¬¡¿´¨'
    #print(cadena.isalpha())
        if not cadena.isalpha():
            for i in caracteres:
                cadena=cadena.replace(i,'')
        return cadena

    def sanitizarCorreo(cadena):
        caracteres='!"#$%&\'()*+,/:;=?@[\]^`{|}~°¬¡¿´¨áéíóúÁÉÍÓÚ'
        #print(cadena.isalpha())
        cadena=str(cadena)
        indiceCaracter=cadena.index('@')
        subcadena=cadena[0:indiceCaracter]
        dominio=cadena[indiceCaracter:]
        #print(subcadena)
        for i in caracteres:
            subcadena=subcadena.replace(i,'')
        return subcadena+dominio

    def validarRFC(cadena):
        caracteres='!"#$%&\'()*+,-./:;=?@[\]^_`{|}~°¬¡¿´¨'
        #print(cadena.isalpha())
        cadena=cadena.upper()
        if not cadena.isalnum():
            for i in caracteres:
                cadena=cadena.replace(i,'')
        return cadena
    
    def validarNumDireccion(cadena):
        caracteres='!"#$%&\'()*+,-./:;=?@[\]^_`{|}~°¬¡¿´¨'
        #print(cadena.isalpha())
        if not cadena.isalnum():
            for i in caracteres:
                cadena=cadena.replace(i,'')
        return cadena
    
    def validarTel(cadena):
        try:
            tel=int(cadena)
            return str(tel)
        except Exception:
            caracteres='0123456789'
            tel=''
            for i in cadena:
                for j in caracteres:
                    if i==j:
                        tel=tel+j
            return tel
    def validarDecimal(cadena):
        try:
            num=float(cadena)
            return str(num)
        except Exception:
            caracteres='0123456789.'
            num=''
            for i in cadena:
                for j in caracteres:
                    if i==j:
                        num=num+j
            return num