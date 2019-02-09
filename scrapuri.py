import urllib.request
import csv

ll = []
print('Entre com a hash do seu Usuário:')
minhahash = input()
for i in range(1,20):
    try:
        page = "https://www.urionlinejudge.com.br/judge/pt/profile/"+minhahash+"?page=" + str(i)
        with urllib.request.urlopen(page) as url:
            s = url.read()
        tt = str(s)
        
        while tt.find('<tr class="par">') != -1 or tt.find('<tr class="impar">') != -1:
            if tt.find('<tr class="par">')<tt.find('<tr class="impar">'):
                tt = tt[tt.find('<tr class="par">')+86:]
            else:
                tt = tt[tt.find('<tr class="impar">')+88:]
            if tt[:4].isdigit():
                ll.append(tt[:4])
    except urllib.error.HTTPError as e:
        ok = True

l = [['No','Tipo', 'feito','Pontos', 'Nível', 'Submissões', 'Resolveram', 'Relação', 'link']]
for i in range(1001,2922):
    try:
        page = "https://www.urionlinejudge.com.br/judge/pt/problems/view/" + str(i)
        with urllib.request.urlopen(page) as url:
            s = url.read()
        tt = str(s)
        t = tt[tt.find('<em class="points">') : tt.find('div class="main-content"')]
        pontos = t[21:t.find(' POINTS')]
        t = t[t.find('target="_blank">')+16:]
        tipo = t[:t.find('</a')]
        
        
        page2 = "https://www.urionlinejudge.com.br/judge/pt/ranks/problem/" + str(i)
        with urllib.request.urlopen(page2) as url:
            s2 = url.read()
        tt2 = str(s2)
        tt2 = tt2[tt2.find('id="problem-statistics">')+24:]
        tt2 = tt2[tt2.find('<p>'):tt2.find('</div>')]
        resolveram = tt2[3:tt2.find('</p>')]
        resolveram = resolveram.replace(".", "")
        tt2 = tt2[tt2.find('<dd>')+4:]
        nivel = tt2[:tt2.find(' ')]
        tt2 = tt2[tt2.find('<dd>')+4:]
        submissoes = tt2[:tt2.find('<')]
        submissoes = submissoes.replace(".", "")
        tt2 = tt2[tt2.find('<dd>')+4:]
        tt2 = tt2[tt2.find('<dd>')+4:]
        relacao = tt2[:tt2.find('.')]
        if str(i) in ll :
            l.append([str(i), str(tipo), str(1), str(pontos), str(nivel), str(submissoes), str(resolveram), str(relacao), page])
        else:
            l.append([str(i), str(tipo), str(0), str(pontos), str(nivel), str(submissoes), str(resolveram), str(relacao), page])
        print(l[len(l)-1])
    except urllib.error.HTTPError as e:
        ok = True

buffer = l

for row_index, list in enumerate(buffer):
    for column_index, string in enumerate(list):
        buffer[row_index][column_index] = buffer[row_index][column_index].replace('\n', '')

with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(buffer)
#I'm guessing this would output the html source code?
