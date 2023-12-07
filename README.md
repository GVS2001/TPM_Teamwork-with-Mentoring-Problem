# TPM_Teamwork-with-Mentoring-Problem

## Resumo
Repositório para o código da Iniciação Científica realizado em 2022/2023, pelo discente Gabriel Vinícius dos Santos (NUSP - 11819424), orientado pela professora Maristela Oliveira dos Santos. O algoritmo foi desenvolvido com o apoio do Conselho Nacional de Desenvolvimento Científico e Tecnológico - CNPq, do Instituto de Ciências Matemáticas e de Computação - ICMC e da Universidade de São Paulo - USP. Os códigos em Python e Python Notebooks foram implementados para resolver o problema (em relação aos 6 diferentes datasets).

## 31º SIICUSP
Com este projeto, pude participar da trigésima primeira edição do SIICUSP - Simpósio Internacional de Iniciação Científica e Tecnológica da USP, obtendo uma experiência inigualável e de alto valor, uma vez que pude conhecer e conversar com muitas outras pessoas de diversas áreas.

## Sobre o Projeto
O foco principal deste trabalho é o desenvolvimento de uma heurística aplicada ao Problema de Trabalho em Equipe com Mentoria (Teamwork with Mentoring Problem - TPM), proposto na competição Google Hash Code de 2022, edição que participei com meus amigos Lucas Fernandes e Pedro Lucas. O TPM envolve a formação de equipes de contribuidores para projetos, considerando as habilidades necessárias para cada projeto e as habilidades dos contribuidores. O objetivo é selecionar uma equipe que maximize a pontuação total dos projetos. Existem restrições rígidas, como a limitação de um contribuidor a um projeto por vez e a disponibilidade dos contribuidores após a conclusão do projeto. Além disso, os profissionais podem ajudar uns aos outros com mentoria, e as habilidades podem aumentar se não atenderem aos requisitos mínimos. Vários projetos podem estar em andamento simultaneamente, com contribuidores ocupando no máximo uma função em cada projeto. Os projetos têm pontuações e datas de vencimento, e a pontuação diminui em um ponto por dia após a data de vencimento. O horizonte de planejamento é definido pela data em que todos os projetos têm pontuação zero. Restrições flexíveis são introduzidas para maximizar a pontuação final. A abordagem de solução para o problema envolve o uso de heurísticas para encontrar soluções iniciais. Posteriormente, um algoritmo é utilizado para aprimorar as soluções, com o foco principal da pesquisa sendo o entendimento aprofundado do TPM e sua resolução, bem como montar boas soluções iniciais, comparando-as com o Estado da Arte.

## Arquivos

### Arquivos no repositório principal: main
- `Apresentação - Problema Google - Mentorship and Teamwork.pdf`: Apresentação feita para explicar o problema para outras pessoas. São slides para motivar e explicar o problema.
- `Mentorship and Teamwork - Hash Code - TPM.pdf`: Enunciado do problema do Google Hash Code de 2022.
- `melhores_pontuacoes.png`: Melhores pontuações e maior valor para cada dataset obtidos da base de dados dos participantes do Google Hash Code de 2022.

### Pasta: datasets
- Contém as 6 instâncias do TPM: as 3 primeiras são mais simples e podem ser resolvidas rapidamente, enquanto as 3 últimas são mais complexas e demoram bastante para ser resolvida.

### Pasta: latex - overleaf
- `Relatório Final - Programação linear inteira para resolução do problema de formação de equipes `: arquivo pdf e zip latex e overleaf para o relatório final enviado ao Cnpq para conclusão da IC.
- `SIICUSP - Otimização linear inteira para resolução do problema de formação de equipes_ otimização de múltiplas equipes com mentoria`: arquivo pdf e zip latex e overleaf para resumo do 31º SIICUSP em português.
- `SIICUSP___Integer_Linear_Optimization_for_Solving_the_Team_Formation_Problem__Multi_Team_Mentoring_Optimization`: arquivo pdf e zip latex e overleaf: arquivo pdf e zip latex e overleaf para resumo do 31º SIICUSP em inglês.

### Pasta: src (source)
- `Gráficos_SIICUSP.ipynb`: Códigos feitos em Python e Python Notebooks para gerar gráficos de visualização dos resultados
- `IC_Final.ipynb`: Código principal feito em Python e Python Notebooks, incluindo a função solver, função de pontuação, etc. As heurísticas são escolhidas devido aos parametros na função solver.
- `IC_resultados.ipynb`: Código feito em Python e Python Notebooks usado para gerar os melhores resultados, que foram presentes nos relatórios. Todas as instâncias foram testadas diversas vezes, e os melhores resultados obtidos foram anotados.
- `Visualização Exploratória - IC.ipynb`: Código feito em Python e Python Notebooks para gerar visualizações exploratórias, de modo a tirar insights dos dados e das instâncias.

## Agradecimentos
Primeiramente e mais importante, a professora orientadora Maristela Oliveira dos Santos, cuja orientação, conhecimento e apoio foram fundamentais para o desenvolvimento deste trabalho. Também estendo minha gratidão aos amigos e colaboradores que compartilharam ideias valiosas e feedback construtivo ao longo desta jornada de pesquisa, junto com minha família e amigos pelo constante incentivo e apoio emocional. Reconheço também o apoio das Instituições que deram vida a este projeto, como o Conselho Nacional de Desenvolvimento Científico e Tecnológico - Cnpq, o Instituto de Ciências Matemáticas e de Computação - ICMC, e a Universidade de São Paulo - USP. Este estudo, que começou como um sonho meu de resolver o presente problema, não teria sido possível sem o apoio e a colaboração de todos vocês. Muito obrigado.
