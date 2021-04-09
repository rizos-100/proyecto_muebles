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