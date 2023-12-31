from flask import Flask, render_template, request
from sklearn.metrics import jaccard_score

app = Flask(__name__)

def chuoi_dauvao(text):
    return text.lower().split()

def tinhdotuongdong_jaccard(vanban_1, vanban_2):
    chuoi_1 = chuoi_dauvao(vanban_1)
    chuoi_2 = chuoi_dauvao(vanban_2)

    try:
        dotuongdong_jaccard = jaccard_score(chuoi_1, chuoi_2, average='micro')
    except ValueError:
        dotuongdong_jaccard = 0.0

    tugiongnhau = set(chuoi_1) & set(chuoi_2)
    tukhacnhau_vb1 = set(chuoi_1) - set(chuoi_2)
    tukhacnhau_vb2 = set(chuoi_2) - set(chuoi_1)

    return dotuongdong_jaccard, tugiongnhau, tukhacnhau_vb1, tukhacnhau_vb2

def khoangcach_levenshtein(a, b):
    dodai_vb1, dodai_vb2 = len(a), len(b)

    dp = [[0] * (dodai_vb2 + 1) for _ in range(dodai_vb1 + 1)]

    for i in range(dodai_vb1 + 1):
        for j in range(dodai_vb2 + 1):
            dp[i][j] = j if i == 0 else (i if j == 0 else min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + (0 if a[i-1] == b[j-1] else 1)))

    return dp[dodai_vb1][dodai_vb2]

def tinhdotuongdong_levenshtein(vanban_1, vanban_2):
    khoangcach = khoangcach_levenshtein(vanban_1, vanban_2)
    chuoidainhat = max(len(vanban_1), len(vanban_2))
    dotuongdong = 1 - (khoangcach / chuoidainhat)

    return dotuongdong, set(vanban_1.lower().split()) & set(vanban_2.lower().split()), set(vanban_1.lower().split()) - set(vanban_2.lower().split()), set(vanban_2.lower().split()) - set(vanban_1.lower().split())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result_jaccard', methods=['POST'])
def result_jaccard():
    vanban_1 = request.form['vanban_1']
    vanban_2 = request.form['vanban_2']

    dotuongdong_jaccard, tugiongnhau, tukhacnhau_vb1, tukhacnhau_vb2 = tinhdotuongdong_jaccard(vanban_1, vanban_2)

    return render_template('result.html', dotuongdong=dotuongdong_jaccard,
                           tugiongnhau=tugiongnhau, tukhacnhau_vb1=tukhacnhau_vb1,
                           tukhacnhau_vb2=tukhacnhau_vb2, vanban_1=vanban_1, vanban_2=vanban_2, method="Jaccard")

@app.route('/result_levenshtein', methods=['POST'])
def result_levenshtein():
    vanban_1 = request.form['vanban_1']
    vanban_2 = request.form['vanban_2']

    ketqua_levenshtein = tinhdotuongdong_levenshtein(vanban_1, vanban_2)
    dotuongdong_levenshtein = ketqua_levenshtein[0]
    tugiongnhau_levenshtein = ketqua_levenshtein[1]
    tukhacnhau_vb1_levenshtein = ketqua_levenshtein[2]
    tukhacnhau_vb2_levenshtein_levenshtein = ketqua_levenshtein[3]

    diemkitu_vb1, diemkitu_vb2 = len(vanban_1), len(vanban_2)

    return render_template('result.html', dotuongdong=dotuongdong_levenshtein,
                           tugiongnhau=tugiongnhau_levenshtein, tukhacnhau_vb1=tukhacnhau_vb1_levenshtein,
                           tukhacnhau_vb2=tukhacnhau_vb2_levenshtein_levenshtein, diemkitu_vb1=diemkitu_vb1, diemkitu_vb2=diemkitu_vb2,
                           vanban_1=vanban_1, vanban_2=vanban_2, method="Levenshtein")

if __name__ == '__main__':
    app.run(debug=True)