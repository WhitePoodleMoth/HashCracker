# 🔐 HashCracker

## 📘 Sobre o projeto
HashCracker é uma ferramenta de força bruta para decodificação de hashes codificados. Utilizando este script em Python, você pode gerar combinações de palavras a partir de conjuntos de caracteres predefinidos e tentar decodificar vários tipos de hashes, incluindo MD5, SHA1, SHA224, SHA256, SHA384, SHA512, BLAKE2B e BLAKE2S.

## 🔧 Construção do Sistema
O sistema foi construído em Python, com um design voltado para o uso eficiente de várias threads em paralelo. Uma única thread é responsável por alimentar uma lista de palavras, que é processada simultaneamente pelas demais threads conforme disponibilidade. Cada thread gera hashes para cada palavra da lista e os compara com os hashes armazenados, continuando até que todas as possíveis correspondências sejam encontradas. As soluções encontradas são gravadas num arquivo ao longo do processo, otimizando o registro do progresso.

## 📋 Requisitos para Utilizar o Sistema

Para executar o HashCracker, você precisa ter os seguintes softwares instalados:

- 🐍 Python 3.8+
- 📚 Git

Também é necessário que o usuário tenha familiaridade com o terminal.

## 🚀 Como Usar

1. Primeiro, clone o repositório:
```bash
git clone https://github.com/WhitePoodleMoth/HashCracker.git
```

2. Navegue até a pasta do projeto:
```bash
cd HashCracker
```

3. Você pode editar o arquivo `main.py` ou criar o seu próprio

```python
import HC.BFH
lista_hash = ["fcd6eb393e783a20e3db79db0ef57c49","b845f8a24f6821855a4cba4c5a422416"]
_hc = HC.BFH.HashCracker(lista_hash,"MD5",10,500,3)
_hc.Crack()
_hc.Checker()
```

4. Agora você pode executar o script:
```bash
python main.py
```

5. A saída será salva no arquivo `HashCracked.txt`, contendo todos os hashes decodificados.

## 👥 Desenvolvedores
- [WhitePoodleMoth](https://github.com/WhitePoodleMoth)

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.