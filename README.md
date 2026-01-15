# Leitura Musical Interativa e Algorítmica (LeIA)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18259589.svg)](https://doi.org/10.5281/zenodo.18259589)

Interface de geração musical voltada ao estudo de leitura à primeira vista.

### Descrição 
Para o estudo de leitura à primeira vista, o estudante defronta-se com a necessidade de selecionar excertos de repertório, exemplos de livros didáticos ou utilizar softwares de teoria musical. Nos três casos, a delimitação do contexto rítmico-harmônico é essencial para o desenvolvimento de metodologias adequadas às dificuldades de cada repertório. O software LeIA (Leitura Musical Interativa e Algorítmica) fora elaborado tendo este horizonte em vista: excertos musicais são gerados a partir da seleção de modelos harmônicos e padrões rítmicos, de modo que o estudante possa concentrar o estudo em certos elementos de percepção (e.g. modos eclesiásticos, estruturas tonais, séries dodecafônicas e combinações rítmicas complexas).

## Instalação
1. Crie e acesse o diretório que deseja instalar LeIA.
2. Clone ou realize o download dos arquivos do repositório.
3. Instale os requisitos mínimos no sistema.
4. Configure e ative um ambiente virtual python (se aplicável)
5. Instale as dependências.
### Exemplo em Debian
```bash
#Crie e acesse um diretório
dir=~/LeIA_LeituraMusical
mkdir -p $dir && cd $dir

#Download do repositório
git clone https://github.com/xafer-gab/LEIA.git
cd LEIA

#Instalação de Lilypond e Fluidsynth
sudo apt install -y lilypond fluidsynth

#Configurar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate

#Instalar bibliotecas requeridas
pip install -r requirements.txt
```

## Inicialização
Para iniciar o programa, basta executar o arquivo <code>main.py</code> localizado no diretório principal do projeto. A interface gradio será carregada e exibirá uma mensagem no terminal. Abra o link fornecido em seu browser para acessar a interface de LeIA.
```bash
#Executa o script de inicialização
python main.py
```


## Uso
O software LeIA apresenta uma interface baseada em web (gradio) em que é possível selecionar um amplo conjunto de parâmetros para a geração de exemplos musicais. 


Os parâmetros consistem em:

1. conjunto de escalas que abrange as linguagens tonais, modais e atonais;
2. combinação de durações selecionáveis;
3. seleção de fórmulas de compasso simples, compostas e irregulares (5/8, 7/16, etc.);
4. seleção do número de oitavas;
5. seleção entre clave de Sol, Fá e Dó e percussão;
6. seleção do número de compassos gerados a cada exercício;
7. modelo harmônico probabilístico (distribuição igual, tonal, serial, etc.);
8. porcentagem de pausas em cada exercício;
9. Dispersão melódica ou chance de salto entre oitavas;
10. Ajuste de andamento e timbre para reprodução MIDI.

Após selecionar os parâmetros da geração, clicar em "gerar" para produzir o próximo exercício de leitura.

## Referências
XAVIER, Gabriel. **Leitura Musical Interativa e Algorítmica (LeIA)**: software livre para o estudo de leitura à primeira vista. Relatório Técnico. Zenodo, 2026. Disponível em: https://doi.org/10.5281/zenodo.18258255.

XAVIER, Gabriel. **LeIA: Leitura Musical Interativa e Algorítmica (v1.0.0)**. Zenodo, 2026. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18259589.svg)](https://doi.org/10.5281/zenodo.18259589)






