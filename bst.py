class AVL:
    def __init__(self):
        self.__raiz = None
        self.soma = 0

    class No:
        def __init__(self, pai, valor):
            self.pai = pai
            self.esquerda = None
            self.direita = None
            self.valor = valor
            self.altura = 1

        def __str__(self):
            return str(self.valor)

        def __repr__(self):
            return self.__str__()

    def minimo(self, atual=None):
        # se atual n�o tem valor inicial, come�ar da raiz
        if atual is None:
            atual = self.__raiz

        # enquanto houver um filho a esquerda, caminhar nessa dire��o
        while atual.esquerda is not None:
            atual = atual.esquerda

        # n�o tem mais filho a esquerda
        # ent�o atual � o menor elemento da �rvore
        return atual

    def maximo(self, atual=None):
        # se atual n�o tem valor inicial, come�ar da raiz
        if atual is None:
            atual = self.__raiz

        # enquanto houver um filho a direita, caminhar nessa dire��o
        while atual.direita is not None:
            atual = atual.direita

        # n�o tem mais filho a direita
        # ent�o atual � o maior elemento da �rvore
        return atual

    def buscar(self, valor):
        atual = self.__raiz

        # enquanto atual existir e o valor for diferente do desejado
        # ir descendo na �rvore pela esquerda (se for menor)
        # ou pela direita (se for maior)
        while atual is not None and valor != atual.valor:
            if valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita

        # se encontrou, atual � o pr�prio n�
        # caso contr�rio, atual � None
        return atual

    def buscar_recursivo(self, valor):

        def recursao(atual, valor):

            # � igual ou nulo?
            if valor == atual.valor or atual is None:
                # se encontrou, atual � o pr�prio n� buscado
                # caso contr�rio, atual � None
                return atual

            if valor < atual.valor:
                # se o valor buscado for menor que o atual
                # buscar na sub-�rvore da esquerda
                return recursao(atual.esquerda, valor)
            else:
                # se o valor buscado for maior que o atual
                # buscar na sub-�rvore da direita
                return recursao(atual.direita, valor)

        return recursao(self.__raiz, valor)

    def inserir(self, valor):

        pai_atual = None
        atual = self.__raiz  # come�ando pela raiz
        novo = self.No(None, valor)  # criando o novo n� com o valor

        while atual is not None:
            pai_atual = atual

            if novo.valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita

        novo.pai = pai_atual
        self.soma += novo.valor

        if pai_atual is None:
            self.__raiz = novo
        elif novo.valor < pai_atual.valor:
            pai_atual.esquerda = novo
        else:
            pai_atual.direita = novo

        self.rebalanciar(novo)

    def rebalanciar(self, no):
        while no is not None:
            self.atualizarAltura(no)

            if self.getAltura(no.esquerda) >= 2 + self.getAltura(no.direita):
                # rota��o a direita
                if self.getAltura(no.esquerda.esquerda) >= self.getAltura(no.esquerda.direita):
                    self.rotacaoDireita(no)
                # rota��o dupla a direita
                else:
                    self.rotacaoEsquerda(no.esquerda)
                    self.rotacaoDireita(no)
            elif self.getAltura(no.direita) >= 2 + self.getAltura(no.esquerda):
                # rota��o a esquerda
                if self.getAltura(no.direita.direita) >= self.getAltura(no.direita.esquerda):
                    self.rotacaoEsquerda(no)
                # rota��o dupla a esquerda
                else:
                    self.rotacaoDireita(no.direita)
                    self.rotacaoEsquerda(no)

            no = no.pai


    def getAltura(self, no):
        if no is None:
            return -1
        return no.altura

    def atualizarAltura(self, no):
        no.altura = max(self.getAltura(no.esquerda), self.getAltura(no.direita)) + 1

    def rotacaoEsquerda(self, no):
        y = no.direita
        y.pai = no.pai

        if y.pai is None:
            self.__raiz = y
        else:
            if y.pai.esquerda is no:
                y.pai.esquerda = y
            elif y.pai.direita is no:
                y.pai.direita = y

        no.direita = y.esquerda
        if no.direita is not None:
            no.direita.pai = no

        y.esquerda = no
        no.pai = y

        self.atualizarAltura(no)
        self.atualizarAltura(y)

    def rotacaoDireita(self, no):

        y = no.esquerda
        y.pai = no.pai
        if y.pai is None:
            self.__raiz = y
        else:
            if y.pai.esquerda is no:
                y.pai.esquerda = y
            elif y.pai.direita is no:
                y.pai.direita = y

        no.esquerda = y.direita
        if no.esquerda is not None:
            no.esquerda.pai = no

        y.direita = no
        no.pai = y

        self.atualizarAltura(no)
        self.atualizarAltura(y)


    def sucessor(self, valor):
        atual = self.buscar(valor)

        # se o elemento n�o existe, n�o possui sucessor
        if atual is None:
            return atual

        if atual.direita is not None:
            # (� uma busca de cima pra baixo)
            return self.minimo(atual.direita)

        pai_atual = atual.pai

        while pai_atual is not None and atual == pai_atual.direita:
            atual = pai_atual
            pai_atual = pai_atual.pai

        # sem sucessor
        if pai_atual is None:
            return pai_atual

        # com sucessor
        return pai_atual

    def predecessor(self, valor):
        atual = self.buscar(valor)

        # se o elemento n�o existe, n�o possui predecessor
        if atual is None:
            return atual

        # se existir uma sub-�rvore a esquerda
        # o predecessor ser� o elemento da extrema direita dessa sub-�rvore
        if atual.esquerda is not None:
            # (� uma busca de cima pra baixo)
            return self.maximo(atual.esquerda)

        pai_atual = atual.pai

        while pai_atual is not None and atual == pai_atual.esquerda:
            # subindo um n�vel hier�rquico por repeti��o
            atual = pai_atual
            pai_atual = pai_atual.pai

        # sem predecessor
        if pai_atual is None:
            return pai_atual

        # com predecessor
        return pai_atual

    def apagar(self, valor):
        sera_removido = self.buscar(valor)

        if sera_removido.esquerda is None:
            self.recortar(sera_removido, sera_removido.direita)
        elif sera_removido.direita is None:
            self.recortar(sera_removido, sera_removido.esquerda)
        else:
            sucessor = self.sucessor(sera_removido.valor)

            if sucessor.pai != sera_removido:
                self.recortar(sucessor, sucessor.direita)

                sucessor.direita = sera_removido.direita
                sucessor.direita.pai = sucessor

            self.recortar(sera_removido, sucessor)

            # a sub-�rvore da esquerda do n� recortado ser� a que pertencia ao n� removido
            sucessor.esquerda = sera_removido.esquerda
            sucessor.esquerda.pai = sucessor

        self.rebalanciar(sera_removido.pai)

    # recorta um n� para o lugar do n� removido (o pai do recortado � atualizado)
    # o n� recortado n�o carrega os filhos
    def recortar(self, sera_removido, sera_recortado):
        if sera_removido.pai is None:
            # se o n� a ser removido n�o tiver pai, a raiz est� sendo removida
            # o n� que ser� colocado no lugar ser� a nova raiz
            self.__raiz = sera_recortado
        elif sera_removido == sera_removido.pai.esquerda:
            # removendo um n� que � o filho a esquerda
            sera_removido.pai.esquerda = sera_recortado
        else:
            # removendo um n� que � o filho a direita
            sera_removido.pai.direita = sera_recortado

        if sera_recortado is not None:
            # o pai do que foi removido ser� pai agora do n� que foi para seu lugar
            sera_recortado.pai = sera_removido.pai

    def listar(self):
        # ir� retornar uma lista ordenada
        lista = []

        def em_ordem(atual):
            if atual is not None:
                em_ordem(atual.esquerda)
                lista.append(atual.valor)  # cadastrando atual
                em_ordem(atual.direita)

        em_ordem(self.__raiz)

        return lista

    def preOrder(self, root):

        if not root:
            return

        print("{0} ".format(root.valor), end="")
        self.preOrder(root.esquerda)
        self.preOrder(root.direita)

    def getRaiz(self):
        return  self.__raiz

arvore = AVL()

# arvore.inserir(5)
# arvore.inserir(8)
# arvore.inserir(9)
# arvore.inserir(7)
# arvore.inserir(6)
# arvore.inserir(2)

arvore.inserir(10)
arvore.inserir(20)
arvore.inserir(30)
arvore.inserir(40)
arvore.inserir(50)
arvore.inserir(25)
a = arvore.getRaiz()
print(a.esquerda)