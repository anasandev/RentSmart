# RentSmart

Aplicação de terminal para calcular orçamentos de aluguel da imobiliária
fictícia R.M Imóveis e gerar uma projeção financeira de 12 meses.

## Requisitos

- Python 3.10 ou superior.
- Sem dependências externas.

## Executar

Abra a pasta do projeto no VS Code, abra **Terminal > Novo Terminal** e execute:

```powershell
python main.py
```

Se necessário, use `py -3 main.py`. Responda às perguntas do menu. O orçamento
aparece no terminal e o CSV é salvo em `resultados/projecao_rentsmart.csv`.

## Ver a projeção em tabela

No PowerShell, na pasta do projeto, execute:

```powershell
Import-Csv .\resultados\projecao_rentsmart.csv | Format-Table -AutoSize
```

No VS Code, use **Ctrl+Shift+P > Tasks: Run Task > Mostrar projeção CSV no
terminal**. Execute o programa primeiro para gerar o CSV.

## Testes

```powershell
python -m unittest discover -s tests -v
```

## Arquivos

- `main.py`: menu e execução.
- `imovel.py`, `apartamento.py`, `casa.py`, `studio.py`: classes dos imóveis.
- `orcamento.py`: cálculos do orçamento.
- `projecao.py`: geração do CSV.
- `.vscode/tasks.json`: tarefa para exibir o CSV em tabela no VS Code.
- `DOCUMENTACAO.md`: documentação teórica.
- `PITCH.md`: roteiro de apresentação.
