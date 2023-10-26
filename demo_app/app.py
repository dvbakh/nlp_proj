
from flask import Flask, render_template, request
app = Flask(__name__)
import sqlite3
import unicodedata
import stanza

stz = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma')

def exact_word(some_word):
    conn = sqlite3.connect('my_corpus (2).db')
    cur = conn.cursor()
    data = """
    SELECT db_meta.page_number, sentence, words, title FROM db_meta
    JOIN db_corp ON db_meta.page_number = db_corp.page_number
    """
    seen=[]
    cur.execute(data)
    textts=cur.fetchall()
    for row in textts:
        lst_rows=row[2].split()
        for n_l in range(len(lst_rows)):
            wrd=lst_rows[n_l].split('=')
            if wrd[0] == some_word[1:-1]:
                if n_l+2 < len(lst_rows):
                    seen.append([row[1], row[3], lst_rows[n_l+1], lst_rows[n_l+2]])
                elif n_l+1 < len(lst_rows):
                    seen.append([row[1], row[3], lst_rows[n_l+1], 'null'])
                else:
                    seen.append([row[1], row[3], 'null', 'null'])
    conn.close()
    return(seen)

def lemma_word(some_word):
    conn = sqlite3.connect('my_corpus (2).db')
    cur = conn.cursor()
    data = """
    SELECT db_meta.page_number, sentence, words, title FROM db_meta
    JOIN db_corp ON db_meta.page_number = db_corp.page_number
    """
    seen=[]
    cur.execute(data)
    textts=cur.fetchall()
    doc=stz(some_word)
    for sent in doc.sentences:
        for word in sent.words:
            some_word_lem=word.lemma
    for row in textts:
        k=0
        lst_rows=row[2].split()
        for n_l in range(len(lst_rows)):
            k+=1
            wrd=lst_rows[n_l].split('=')
            if wrd[2] == some_word_lem:
                if n_l+2 < len(lst_rows):
                    seen.append([row[1], row[3], lst_rows[n_l+1], lst_rows[n_l+2]])
                elif n_l+1 < len(lst_rows):
                    seen.append([row[1], row[3], lst_rows[n_l+1], 'null'])
                else:
                    seen.append([row[1], row[3], 'null', 'null'])
    conn.close()
    return(seen)

def word_and_pos(some_word):
    some_word=some_word.split('+')
    conn = sqlite3.connect('my_corpus (2).db')
    cur = conn.cursor()
    data = """
    SELECT db_meta.page_number, sentence, words, title FROM db_meta
    JOIN db_corp ON db_meta.page_number = db_corp.page_number
    """
    seen=[]
    cur.execute(data)
    textts=cur.fetchall()
    for row in textts:
        lst_rows=row[2].split()
        for n_l in range(len(lst_rows)):
            wrd=lst_rows[n_l].split('=')
            if wrd[0] == some_word[0] and wrd[1] == some_word[1]:
                if n_l+2 < len(lst_rows):
                    seen.append([row[1], row[3], lst_rows[n_l+1], lst_rows[n_l+2]])
                elif n_l+1 < len(lst_rows):
                    seen.append([row[1], row[3], lst_rows[n_l+1], 'null'])
                else:
                    seen.append([row[1], row[3], 'null', 'null'])
    conn.close()
    return(seen)
    
def pos_word(pos):
    conn = sqlite3.connect('my_corpus (2).db')
    cur = conn.cursor()
    data = """
    SELECT db_meta.page_number, sentence, words, title FROM db_meta
    JOIN db_corp ON db_meta.page_number = db_corp.page_number
    """
    seen=[]
    cur.execute(data)
    textts=cur.fetchall()
    for row in textts:
        lst_rows=row[2].split()
        for n_l in range(len(lst_rows)):
            wrd=lst_rows[n_l].split('=')
            if wrd[1] == pos:
                if n_l+2 < len(lst_rows):
                    seen.append([row[1], row[3], lst_rows[n_l+1], lst_rows[n_l+2]])
                elif n_l+1 < len(lst_rows):
                    seen.append([row[1], row[3], lst_rows[n_l+1], 'null'])
                else:
                    seen.append([row[1], row[3], 'null', 'null'])
    conn.close()
    return(seen)
    
def for_one_word(word_s):
    frst_wrd=[]
    if word_s[0]=='"':
        for i in exact_word(word_s):
            frst_wrd.append([i[0], i[1], i[2], i[3]])
    elif word_s[0] in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        for i in pos_word(word_s):
            frst_wrd.append([i[0], i[1], i[2], i[3]])
    elif len(word_s.split('+'))==2:
        for i in word_and_pos(word_s):
            frst_wrd.append([i[0], i[1], i[2], i[3]])
    else:
        for i in lemma_word(word_s):
            frst_wrd.append([i[0], i[1], i[2], i[3]])
    return(frst_wrd)
    
def for_two_words(word_s):
    two_wrds=[]
    for o in for_one_word(word_s[0]):
        if word_s[1][0]=='"':
            if o[2].split('=')[0] == word_s[1][1:-1]:
                two_wrds.append(o)
        elif word_s[1][0] in 'QWERTYUIOPASDFGHJKLZXCVBNM':
            if o[2].split('=')[1] == word_s[1]:
                two_wrds.append(o)
        elif len(word_s[1].split('+'))==2:
            if o[2].split('=')[1] == word_s[1].split('+')[1] and o[2].split('=')[0] == word_s[1].split('+')[0]:
                two_wrds.append(o)
        else:
            doc=stz(word_s[1])
            for sent in doc.sentences:
                for word in sent.words:
                    word_lem=word.lemma
            if o[2].split('=')[2] == word_lem:
                two_wrds.append(o)
    return(two_wrds)
    
def for_three_words(word_s):
    three_wrds=[]
    for o in for_two_words(word_s[:2]):
        if word_s[2][0]=='"':
            if o[3].split('=')[0] == word_s[2][1:-1]:
                three_wrds.append(o)
        elif word_s[2][0] in 'QWERTYUIOPASDFGHJKLZXCVBNM':
            if o[3].split('=')[1] == word_s[2]:
                three_wrds.append(o)
        elif len(word_s[2].split('+'))==2:
            if o[3].split('=')[1] == word_s[2].split('+')[1] and o[3].split('=')[0] == word_s[2].split('+')[0]:
                three_wrds.append(o)
        else:
            doc=stz(word_s[2])
            for sent in doc.sentences:
                for word in sent.words:
                    word_lem=word.lemma
            if o[3].split('=')[2] == word_lem:
                three_wrds.append(o)
    return(three_wrds)
    

@app.route("/")
def main():
    return render_template('index.html')
    
@app.route('/search',methods=['POST'])
def search():
    # read the posted values from the UI 
    word = request.form['words']
    sea=word.split()
    def searchh(inp):
        d=[]
        if len(inp) == 1:
            for o in for_one_word(inp[0]):
                if o[0] not in d:
                    d.append(o)
        elif len(inp) == 2:
            for o in for_two_words(inp[:2]):
                if o[0] not in d:
                    d.append(o)
        elif len(inp) == 3:
            for o in for_three_words(inp[:3]):
                if o[0] not in d:
                    d.append(o)
        return d
    data=searchh(sea)
    if len(data) != 0:
        return render_template('out.html', data=data, seearch=word)
    else:
        return render_template('err.html')
        
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)