#returns page as string
def readpage(page):
    try:
        s = ur.Request(page, headers={'User-Agent': 'Mozilla/5.0'})
        tt = ur.urlopen(s).read()
        return str(tt)
    except HTTPError:
        return " "
#returns the problem ids from the profile page
def numberseparator(tt):
    ll = []
    while tt.find('<a href="/judge/pt/problems/view/') != -1:
        q = tt.find('<a href="/judge/pt/problems/view/') + 33
        if tt[q:q+4] not in ll:
            ll.append(tt[q:q+4])
        tt = tt[q:]
    return ll
#return list of all problems with various status
def listall(ll):
    l = [['No','Tipo', 'feito','Pontos', 'Nível', 'Submissões', 'Resolveram', 'Relação', 'link']]
    for i in range(1001,2949):
        page = "https://www.urionlinejudge.com.br/judge/pt/problems/view/" + str(i)
        tt = readpage(page)
        t = tt[tt.find('<em class="points">') : tt.find('div class="main-content"')]
        if t.find(' PONTOS') != -1:
            pontos = t[21:t.find(' PONTOS')]
        else:
            pontos = t[21:t.find(' POINTS')]
        t = t[t.find('target="_blank">')+16:]
        tipo = t[:t.find('</a')]
        
        
        page2 = "https://www.urionlinejudge.com.br/judge/pt/ranks/problem/" + str(i) + "/2"
        tt2 = readpage(page2)
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
        progress(i-1000,1949)
    return l
#gives progress bar. from https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


import urllib.request as ur
from urllib.error import HTTPError
import csv
import sys


def main():
    ll = []
    #Entre com a hash do seu Usuário
    minhahash = "211459"
    i = 1
    while True:
        page = "https://www.urionlinejudge.com.br/judge/pt/profile/"+minhahash+"?page=" + str(i) + "&sort=Ranks.problem_id&direction=asc"
        tt = readpage(page)
        if tt == " ": break
        ll = ll + numberseparator(tt)
        i +=1
    buffer = listall(ll)
    
    #generates csv file
    for row_index, list in enumerate(buffer):
        for column_index, string in enumerate(list):
            buffer[row_index][column_index] = buffer[row_index][column_index].replace('\n', '')
    
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(buffer)
        
if __name__ == '__main__':
    main()
