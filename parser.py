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

        #Miramos si el siguiente es una declaracion de
        # variables

        nextTok = self.nextToken()

        if nextTok == 'VAR':
            self.paseVARDEC()

        nextTok = self.nextToken() 
        
        if nextTok == 'PROC':
            self.parsePROCSDEF()

        #TODO: VERIFICAR SI EL BLOQUE ES OBLIGATORIO 
        self.parseINSB()

        self.accept('GORP')

    def parsePROCSDEF():

        self.parsePROCDEF()
        
        nextTok = self.nextToken()
        if nextTok == 'PROC':
            self.parsePROCSDEF()

    def parsePROCDEF():
        self.accept('PROC')
        self.parseNAME()
        self.parseLISTPARAMS()
        self.accept('{')
        self.parseINSS()
        self.accept('}')
        self.accept('CORP')

    def parseVARDEC():
        self.accept('VAR')
        self.parseLISTNAM()
        self.accept(';')

    
         
        nexTok = self.nextToken()

        if nexTok == '(':
            self.accept('(')
            self.parseINS()
            self.accept(')')
            self.parseS()
        # De lo contrario únicamente una instruccion 
        else:
            self.parseINS()

        # Consumir ')'

        self.accept(')')

        # Validamos si hay más instrucciones
        nexTok = self.nextToken()
        if nexTok == '(':
            self.parseS()


    def parseINS(self):
        nexTok = self.nextToken()

        #Casos para comandos

        if nexTok == 'defvar':
            self.accept('defvar')
            var = self.nextToken()
            self.user_variables.append(var)
            self.parseNAME()
            self.parseNUM()
            pass
        
        elif nexTok == '=':
            self.accept('=')
            self.parseVAR()
            self.parseNUM()

        elif nexTok == 'move':
            self.accept('move')
            self.parseVARNUM()

        elif nexTok == 'turn':
            self.accept('turn')
            self.parseD()

        elif nexTok == 'face':
            self.accept('face')
            self.parseO()

        elif nexTok == 'put':
            self.accept('put')
            self.parseX()
            self.parseVARNUM()

        elif nexTok == 'pick':
            self.accept('pick')
            self.parseX()
            self.parseVARNUM()

        elif nexTok == 'rundirs':
            self.accept('rundirs')
            self.parseDs()

        elif nexTok == 'move-face':
            self.accept('move-face')
            self.parseNUM()
            self.parseO()

        elif nexTok == 'skip':
            self.accept('skip')

        # Casos para las estructuras de control

        elif nexTok == 'if':
            self.accept('if')
            self.parseCOND()
            self.parseBLOCK()
            self.parseBLOCK()

        elif nexTok == 'loop':
            self.accept('loop')
            self.parseCOND()
            self.parseBLOCK()

        elif nexTok == 'repeat':
            self.accept('repeat')
            self.parseVARNUM()
            self.parseBLOCK

        elif nexTok == 'defun':
            self.accept('defun')
            #Incluir la función en la lista de funcione
            # definidas por el usuario

            func_name = self.nextToken()
            self.user_functions[func_name] = []

            #Continuar el parseo

            self.parseNAME()
            self.accept('(')
            self.parseARGS(func_name)
            self.accept(')')
            pre_contex_vars = self.user_variables.copy()

            #Se le agregan las nuevas variables al contexto
            self.user_variables += self.user_functions[func_name] 
            self.parseS()
            
            #Se sacan las variables del contexto
            self.user_variables = pre_contex_vars

        # Casos para funciones definidas por el usuario 

        elif nexTok in self.user_functions.keys():
            self.parseFUN()
            self.parseUDFARGS(nexTok)

        else:
            raise Exception('TOKEN NO RECONOCIDO- FUNCIÓN NO RECONOCIDA')

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