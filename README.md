# loterias.json

Todos os resultados das Loterias Caixa em formato JSON.

O sistema coleta automaticamente os resultados históricos e se mantém atualizado através de um GitHub Action que roda diariamente.

## Serviços Disponíveis

- Mega-Sena
- Quina
- Lotofácil
- Lotomania
- Dupla Sena (inclui 1º e 2º sorteios)
- Timemania (inclui Time do Coração)
- Dia de Sorte
- Federal
- +Milionária (inclui Trevos)
- Super Sete
- Mega-Sena da Virada (sorteios de 31/12)

## Formato dos Dados

Cada loteria possui seu arquivo `.json` na pasta `data/`. O formato geral é:

```json
{
  "concurso": 1,
  "data": "DD/MM/YYYY",
  "resultado": ["01", "02", ...]
}
```
*O resultado é dado na ordem crescente.*
*Alguns serviços incluem campos extras como `resultado_2`, `trevos` ou `time_do_coracao`.*

## Acesso

Obtenha os dados via GET nos seguintes endpoints:

- Dia de Sorte: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/dia-de-sorte.json
- Dupla Sena: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/dupla-sena.json
- Federal: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/federal.json
- Lotofácil: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/lotofacil.json
- Lotomania: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/lotomania.json
- +Milionária: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/mais-milionaria.json
- Mega-Sena: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/mega-sena.json
- Mega-Sena da Virada: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/mega-sena-da-virada.json
- Quina: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/quina.json
- Super Sete: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/super-sete.json
- Timemania: https://raw.githubusercontent.com/eitchtee/loterias.json/main/data/timemania.json

## Automação

O workflow `.github/workflows/update-data.yml` executa diariamente às 1:00 UTC (22:00 BRT), coleta novos concursos e faz o commit dos arquivos atualizados para o branch `main`.
