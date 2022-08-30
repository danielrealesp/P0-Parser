#################
# AUTHOR: DANIEL REALES
# 201822265
################3


class Tokenizer:

    def __init__(self, text: str) -> None:
        self.program = text 

    def tokenize(self) -> list:
        '''
        Retorna una lista con todos los tokens
        que se encuentran en el texto tokenizar.
        Este último es el atributo text
        '''
        #Agregar espacios y hacer split para obtener la lista de tokens
        ans = self.program.replace('(', ' ( ').replace(')', ' ) ').replace('{', ' { ').replace('}', ' } ').replace(',',' , ').replace(';', ' ; ').replace(':=', ' := ').split()

        result = list(map(lambda x: x.strip(), ans))

        return result 

    def setText(self, text:str):
        self.text = text

class Parser:

    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.user_variables = []
        self.user_functions = {} 

    def parse(self):
        self.parseS()

    def accept(self, token):
        '''
        Verifica que el primer token sea el ingresado
        por parámetro. Si es asi hace lo saca.
        De lo contrario levanta un error
        '''
        try:

            current = self.tokens[0]
            if current == token:
                self.tokens.pop(0)

            else:
                raise Exception('TOKEN NO ESPERADO')

        except IndexError:
            print('PARSING TERMINADO - PROGRAMA VALIDO')
            
    def nextToken(self):
        '''
        Retorna el token siguiente de la lista sin removerlo
        '''
        try:
            return self.tokens[0]

        except IndexError:
            print('PARSING TERMINADO - PROGRAMA VALIDO')

    def parseS(self):
        '''
        Funcion de parse del elemento distinguido
        '''
        self.accept('PROG')

        #Miramos si el siguiente es una declaracion de variables
        nextTok = self.nextToken()

        if nextTok == 'VAR':
            self.parseVARDEC()
        nextTok = self.nextToken() 
        if nextTok == 'PROC':
            self.parsePROCSDEF()
        #TODO: VERIFICAR SI EL BLOQUE ES OBLIGATORIO 
        self.parseINSB()

        self.accept('GORP')

    def parseINSB(self):

        self.accept('{')
        self.parseINSS()
        self.accept('}')

    def parseINSS(self):
        #Terminales de los comandos
        CMDSA = ['M', 'R', 'C', 'B', 'c', 'b', 'P', 'J', 'G']
        #TODO: IMPLEMENTAR LA ASIGNACIÓN
        CMDSB = ['walk', 'jump', 'jumpTo', 'veer', 'look', 'drop', 'grab', 'get', 'free', 'pop']
        CS = ['if', 'while', 'repeatTimes']
        terminales = {'CMDSA': CMDSA, 'CMDSB': CMDSB, "CS": CS}

        self.parseINS(terminales)

        if self.nextToken() != "}":
            self.parseINSS()
    
    def parseCMD(self, terminales):
        nextTok = self.nextToken()
        if nextTok in terminales['CMDSA']:
            self.parseCMDA()

        elif nextTok in terminales['CMDSB']:
            self.parseCMDB()
        self.accept(';')

    # ----------
    # START CMDA
    # ----------

    def parseCMDA(self):
        if self.nextToken() == 'J':
            self.parseJUMP()

        elif self.nextToken() == 'G':
            self.parseGO()

        else: # ['M', 'R', 'C', 'B', 'c', 'b', 'P']
            self.accept(self.nextToken())

    def parseJUMP(self):
        self.accept('J')
        self.accept('(')
        self.parseNUM()
        self.accept(')')

    def parseGO(self):
        self.accept('G')
        self.accept('(')
        self.parseNUM()
        self.accept(',')
        self.parseNUM()
        self.accept(')')

    # --------
    # END CMDA
    # --------

    # ----------
    # START CMDB
    # ----------

    def parseCMDB(self):
        #TODO: Terminar
        nt = self.nextToken()
        
        if nt == 'walk':
            self.accept('walk')
            self.accept('(')

            #Determinar cual de los 3 tipos de Walk es
            o = ['north', 'south', 'east', 'west']
            d2 = ['front', 'right', 'left', 'back']
            nt_new = self.nextToken()  
            if nt_new in o:
                self.parseWALK3()
            elif nt_new in d2:
                self.parseWALK2()
            else:
                self.parseWALK()

        elif nt == 'jump':
            self.parseJUMP2()    
            
        elif nt == 'jumpTo':
            self.parseJUMPTO()
            
        elif nt  == 'veer':
            self.parseVEER()

        elif nt == 'look':
            self.parseLOOK()

        elif nt == 'drop':
            self.parseDROP()

        elif nt == 'grab':
            self.parseGRAB()

        elif nt == 'get':
            self.parseGET()

        elif nt == 'free':
            self.parseFREE()

        elif nt == 'pop':
            self.parsePOP()


    def parseASS(self):
        #TODO
        pass

    def parseWALK(self):
        self.parseVARNUM()
        self.accept(')')

    def parseJUMP2(self):
        self.accept('jump')
        self.accept('(')
        self.parseVARNUM()
        self.accept(')')

    def parseJUMPTO(self):
        self.accept('jumpTo')
        self.accept('(')
        self.parseVARNUM()
        self.accept(',')
        self.parseVARNUM()
        self.accept(')')

    def parseVEER(self):
        self.accept('veer')
        self.accept('(')
        self.parseD()
        self.accept(')')

    def parseD(self):
        D = ['left', 'right', 'around']
        if self.nextToken() in D:
            self.accept(self.nextToken())
        else:
            raise Exception('TOKEN NO RECONOCIDO - DIRECCION INVALIDA')

    def parseLOOK(self):
        self.accept('look')
        self.accept('(')
        self.parseO()
        self.accept(')')
    
    def parseO(self):
        O = ['north', 'south', 'east', 'west']
        if self.nextToken() in O:
            self.accept(self.nextToken())
        else:
            raise Exception('TOKEN NO RECONOCIDO - CARDINALIDAD INVALIDA')

    def parseDROP(self):
        self.accept('drop')
        self.accept('(')
        self.parseVARNUM()
        self.accept(')')

    def parseGRAB(self):
        self.accept('grab')
        self.accept('(')
        self.parseVARNUM()
        self.accept(')')

    def parseGET(self):
        self.accept('get')
        self.accept('(')
        self.parseVARNUM()
        self.accept(')')

    def parseFREE(self):
        self.accept('free')
        self.accept('(')
        self.parseVARNUM()
        self.accept(')')

    def parsePOP(self):
        self.accept('pop')
        self.accept('(')
        self.parseVARNUM()
        self.accept(')')

    def parseWALK2(self):
        self.parseD2()
        self.accept(',')
        self.parseVARNUM()
        self.accept(')')

    def parseD2(self):
        D2 = ['front', 'right', 'left', 'back']
        if self.nextToken() in D2:
            self.accept(self.nextToken())
        else:
            raise Exception('TOKEN NO RECONOCIDO - DIRECCION INVALIDA')

    def parseWALK3(self):
        self.parseO()
        self.accept(',')
        self.parseVARNUM()
        self.accept(')')

    # --------
    # END CMDB
    # --------

    # --------
    # START CS
    # --------

    def parseCS(self):
        if self.nextToken() == 'if':
            self.parseIF()

        elif self.nextToken() == 'while':
            self.parseWHILE()

        elif self.nextToken() == 'repeatTimes':
            self.parseREPEAT()

    def parseIF(self):
        self.accept('if')
        self.accept('(')
        self.parseCOND()
        self.accept(')')
        self.parseBLOCK()
        
        if self.nextToken() == 'else':
            self.accept('else')
            self.parseBLOCK()

        self.accept('fi')
        
    def parseWHILE(self):
        self.accept('while')
        self.accept('(')
        self.parseCOND()
        self.accept(')')
        self.accept('do')
        self.parseBLOCK()
        self.accept('od')

    def parseREPEAT(self):
        self.accept('repeatTimes')
        self.parseVARNUM()
        self.parseBLOCK()
        self.accept('per')

    # ------
    # END CS
    # ------

    # ----------
    # START COND
    # ----------

    def parseCOND(self):
        if self.nextToken() == 'isFacing':
            self.parseISFACING()
        elif self.nextToken() == 'isValid':
            self.parseISVALID()
        elif self.nextToken() == 'canWalk':
            self.parseCANWALK0()
        elif self.nextToken() == 'not':
            self.parseNOT()
        else:
            raise Exception('TOKEN NO RECONOCIDO - CONDICION INVALIDA')

    def parseISFACING(self):
        self.accept('isFacing')
        self.accept('(')
        self.parseO()
        self.accept(')')

    def parseISVALID(self):
        self.accept('isValid')
        self.accept('(')
        self.parseISVINS()
        self.accept(',')
        self.parseVARNUM()
        self.accept(')')

    def parseISVINS(self):
        ins = ['walk', 'jump', 'grab', 'pop', 'pick', 'free', 'drop']
        if self.nextToken() in ins:
            self.accept(self.nextToken())
        else:
            raise Exception('TOKEN NO RECONOCIDO - INSTRUCCION INVALIDA')

    def parseCANWALK0(self):
        canwalk = ['north', 'south', 'east', 'west']
        canwalk2 = ['front', 'right', 'left', 'back']
        
        #TODO: verificar que funcione correctamente por el indice = 2
        if self.tokens[2] in canwalk:
            self.parseCANWALK()
        elif self.tokens[2] in canwalk2:
            self.parseCANWALK2()
        else:
            raise Exception ('TOKEN NO RECONOCIDO - DIRECCION INVALIDA')

    def parseCANWALK(self):
        self.accept('canWalk')
        self.accept('(')
        self.parseO()
        self.accept(',')
        self.parseVARNUM()
        self.accept(')')

    def parseCANWALK2(self):
        self.accept('canWalk')
        self.accept('(')
        self.parseD2()
        self.accept(',')
        self.parseVARNUM()
        self.accept(')')

    def parseNOT(self):
        self.accept('not')
        self.accept('(')
        self.parseCOND()
        self.accept(')')

    # --------
    # END COND
    # --------

    def parsePROCSDEF(self):

        self.parsePROCDEF()
        
        nextTok = self.nextToken()
        if nextTok == 'PROC':
            self.parsePROCSDEF()

    def parsePROCDEF(self):
        self.accept('PROC')

        #Guarda el nombre de la función en la lista e inicializa el
        # número de argumentos a 0

        func_name = self.nextToken()
        self.user_functions[func_name] = 0
        #Consume el nombre
        self.parseNAME()
        self.parseLISTPARAMS(func_name)
        self.parseINSB()
        self.accept('CORP')

    def parseLISTPARAMS(self, func_name: str):
        self.accept("(")
        
        nextTok = self.nextToken()
        if nextTok != ')':
            self.parseLISTNAM('FUNCARG', func_name=func_name)

        self.accept(")")
        
    
    def parseVARDEC(self):
        self.accept('VAR')
        self.parseLISTNAM(type='VARDEC')
        self.accept(';')

    def parseLISTNAM(self, type: str, func_name=None):
        #Agregar la variable a las definidas por el usuario
        nextTok = self.nextToken()
        if type == 'VARDEC':
            self.user_variables.append(nextTok)
        
        elif type == 'FUNCARG':
            if func_name:
                self.user_functions[func_name] += 1

        self.parseNAME()
        nextTok = self.nextToken()
        if nextTok == ',':
            self.accept(',')
            self.parseLISTNAM(type=type, func_name=func_name)

    def parseINS(self, terminales: dict):
        
        nextTok = self.nextToken()

        if nextTok in terminales['CMDSA'] or nextTok in terminales['CMDSB']:
            self.parseCMD(terminales)        

        elif nextTok in terminales['CS']:
            self.parseCS()

        elif nextTok in self.user_functions.keys():
            self.parsePC()

        else:
            raise Exception('TOKEN NO ESPERADO')

    def parseVARNUM(self):
        try:
            val = self.nextToken()
            int(val)
            self.parseNUM()
        except ValueError:
            self.parseVAR()

    def parseBLOCK(self):
        if self.nextToken() == '(':
            self.accept('(')

        self.parseS()
        
        if self.nextToken() == ')':
            self.accept(')')

    def parseCOND(self):
        self.accept('(')

        nexTok = self.nextToken()

        if nexTok == 'facing-p':
            self.accept('facing-p')
            self.parseO()

        elif nexTok == 'can-put-p':
            self.accept('can-put-p')
            self.parseX()
            self.parseVARNUM()

        elif nexTok == 'can-pick-p':
            self.accept('can-pick-p')
            self.parseX()
            self.parseVARNUM()

        elif nexTok == 'can-move-p':
            self.accept('can-move-p')
            self.parseO()

        elif nexTok == 'not':
            self.accept('not')
            self.parseCOND()

        else:
            raise Exception('TOKEN NO RECONOCIDO - CONDICIONAL MAL FORMULADO')

        self.accept(')')

    def parseNAME(self):

        # Únicamente consume el siguiente token

        token = self.nextToken()
        self.accept(token)

    def parseNUM(self):

        #Únicamente consume el siguiente token

        token = self.nextToken()

        # Validar que sea un entero
        int(token)

        self.accept(token)

    def parseVAR(self):

        #Verifica si está en las variables definidas por el usuario
        # En caso afirmativo lo consume

        token = self.nextToken()
        
        if token in self.user_variables:
            self.accept(token)

        else:
            raise Exception('TOKEN NO ESPERADO - LA VARIABLE NO ESTA DEFINIDA')

    def parseD(self):

        nexTok = self.nextToken()
        
        if nexTok == ':left':
            self.accept(':left')

        elif nexTok == ':right':
            self.accept(':right')
        
        elif nexTok == ':around':
            self.accept(':around')

        else:
            raise Exception('TOKEN NO ESPERADO - DIRECCIÓN NO DEFINIDA')


    def parseO(self):

        nexTok = self.nextToken()

        if nexTok == ':north':
            self.accept(nexTok)

        elif nexTok == ':south':
            self.accept(nexTok)

        elif nexTok == ':east':
            self.accept(nexTok)

        elif nexTok == ':west':
            self.accept(nexTok)

        else:
            raise Exception('TOKEN NO ESPERADO - ORIENTACION NO RECONOCIDA')

    def parseX(self):

        nexTok = self.nextToken()

        if nexTok == ':chips':
            self.accept(nexTok)

        elif nexTok == ':ballons':
            self.accept(nexTok)

        else:
            raise Exception('TOKEN NO ESPERADO - OBJETO NO RECONOCIDO')

    def parseDs(self):
        self.accept('(')
        self.parseDss()
        self.accept(')')

    def parseDss(self):
        possibilities = [':left', ':right', ':around']
        self.parseD()
        nextTok = self.nextToken()

        if nextTok in possibilities:
            self.parseDss()

    def parseFUN(self):

        # Únicamente consume el token generado
        self.accept(self.nextToken())

    def parseARGS(self, func_name):

        nexTok = self.nextToken()

        while(nexTok != ')'):
            self.user_functions[func_name].append(nexTok)
            self.accept(nexTok)    
            nexTok = self.nextToken()

    def parseUDFARGS(self, func_name):
        args = self.user_functions[func_name]
        arity = len(args)

        for _ in range(arity):
            self.accept(self.nextToken())


programa = '''
PROG
VAR n, x, y; PROC putCB(c, b)
{
drop(c);
free(b); walk(n)
} CORP
PROC goNorth ()
{
while (canWalk(north ,1)) do { walk(north ,1)} od
} CORP
PROC goWest () {
if (canWalk(west ,1)) { walk(west ,1)} fi
}
CORP
{
go(3,3); n:=6;
putCB (2 ,1)
}
GORP
'''

tokenizer = Tokenizer(programa)
print(tokenizer.tokenize())