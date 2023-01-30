# 이 파이썬 코드는 파이썬 3.11 환경에서 작성했습니다.
# This python code was written in python 3.10 environment.
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import Treeview
from types import NoneType

con = sqlite3.connect('bbwdb_with_id_note_greek_ctre.db')
cur = con.cursor()

DG = nx.DiGraph()

# 데이터베이스의 필드명(튜플)
field = ('id', '언어', '스트롱 넘버', \
    '표기1', '표기2', '표기3', '표기4', \
    '음역1', '음역2', '음역3', '음역4', \
    '발음1', '발음2', '발음3', '발음4', \
    '관련1', '관련2', '관련3', '관련4', \
    '의미1', '의미2', '의미3', '의미4', '의미5', '의미6', '의미7', '비고')

# 데이터베이스의 필드명에 대한 숫자 인덱스(딕셔너리)
field_idx = {'id': 0, '언어': 1, '스트롱': 2, \
    '표기1': 3, '표기2': 4, '표기3': 5, '표기4': 6, \
    '음역1': 7, '음역2': 8, '음역3': 9, '음역4': 10, \
    '발음1': 11, '발음2': 12, '발음3': 13, '발음4': 14, \
    '관련1': 15, '관련2': 16, '관련3': 17, '관련4': 18, \
    '의미1': 19, '의미2': 20, '의미3': 21, '의미4': 22, '의미5': 23, '의미6': 24, '의미7': 25, \
    '비고': 26}

# 데이터베이스의 각 필드명에 대응하는 트리뷰의 각 행 명명(딕셔너리)
field_exp = {'id': 'id', '언어': 'lang', '스트롱': 'strong', \
    '표기1': 'splg1', '표기2': 'splg2', '표기3': 'splg3', '표기4': 'splg4', \
    '음역1': "trsl1", '음역2': "trsl2", '음역3': "trsl3", '음역4': "trsl4", \
    '발음1': "phnt1", '발음2': "phnt2", '발음3': "phnt3", '발음4': "phnt4", \
    '관련1': "rlt1", '관련2': "rlt2", '관련3': "rlt3", '관련4': "rlt4", \
    '의미1': 'mng1', '의미2': 'mng2', '의미3': 'mng3', '의미4': 'mng4', '의미5': 'mng5', '의미6': 'mng6', '의미7': 'mng7', \
    '비고': 'etc,.'}

# 트리뷰 각 행 별 길이 값(딕셔너리)
length = {'id': 80, '언어': 100, '스트롱': 80, '표기':100, '음역': 100, '발음': 80, '관련': 80, \
    '의미': 140, '비고': 70}

# 트리뷰를 통해 표시할 필드의 인덱스(튜플: 딕셔너리에서 원하는 값 불러오기)
tv_show = (field_idx['id'], field_idx['언어'], field_idx['스트롱'], \
    field_idx['표기1'], field_idx['표기2'], field_idx['표기3'], field_idx['표기4'], \
    field_idx['음역1'], field_idx['음역2'], field_idx['음역3'], field_idx['음역4'], \
    field_idx['관련1'], field_idx['관련2'], field_idx['관련3'], field_idx['관련4'], \
    field_idx['의미1'], field_idx['의미2'], field_idx['의미3'], field_idx['의미4'], field_idx['의미5'], field_idx['의미6'], field_idx['의미7'], \
    field_idx['비고'] )

# tv_show = (field_idx['언어'], field_idx['스트롱'], \
#     field_idx['표기1'], field_idx['표기2'], field_idx['표기3'], field_idx['표기4'], \
#     field_idx['음역1'], field_idx['음역2'], field_idx['음역3'], field_idx['음역4'], \
#     field_idx['의미1'], field_idx['의미2'], field_idx['의미3'], field_idx['의미4'], field_idx['의미5'], field_idx['의미6'], field_idx['의미7'], \
#     field_idx['비고'] )

# 트리뷰 행 정의(튜플: 딕셔너리에서 원하는 값 불러오기)
tv_column = (field_exp['id'], field_exp['언어'], field_exp['스트롱'], \
    field_exp['표기1'], field_exp['표기2'], field_exp['표기3'], field_exp['표기4'], \
    field_exp['음역1'], field_exp['음역2'], field_exp['음역3'], field_exp['음역4'], \
    field_exp['관련1'], field_exp['관련2'], field_exp['관련3'], field_exp['관련4'], \
    field_exp['의미1'], field_exp['의미2'], field_exp['의미3'], field_exp['의미4'], field_exp['의미5'], field_exp['의미6'], field_exp['의미7'], \
    field_exp['비고'] )

# tv_column = (field_exp['언어'], field_exp['스트롱'], \
#     field_exp['표기1'], field_exp['표기2'], field_exp['표기3'], field_exp['표기4'], \
#     field_exp['음역1'], field_exp['음역2'], field_exp['음역3'], field_exp['음역4'], \
#     field_exp['의미1'], field_exp['의미2'], field_exp['의미3'], field_exp['의미4'], field_exp['의미5'], field_exp['의미6'], field_exp['의미7'], \
#     field_exp['비고'] )

# 각 행 길이 수치 튜플화(튜플: 딕셔너리에서 원하는 값 불러오기)
tv_clm_len = (length['id'], length['언어'], length['스트롱'], \
    length['표기'], length['표기'], length['표기'], length['표기'], \
    length['음역'], length['음역'], length['음역'], length['음역'], \
    length['관련'], length['관련'], length['관련'], length['관련'], \
    length['의미'], length['의미'], length['의미'], length['의미'], length['의미'], length['의미'], length['의미'], \
    length['비고'] )

# tv_clm_len = (length['언어'], length['스트롱'], \
#     length['표기'], length['표기'], length['표기'], length['표기'], \
#     length['음역'], length['음역'], length['음역'], length['음역'], \
#     length['의미'], length['의미'], length['의미'], length['의미'], length['의미'], length['의미'], length['의미'], \
#     length['비고'] )

nx_node = (field_idx['id'], field_idx['관련1'], field_idx['관련2'], field_idx['관련3'], field_idx['관련4'])

# can_w_h = (700, 300) # 캔버스 너비, 높이(튜플)

####################################################################################################
# 여기부터 클래스와 함수 관련 코드
####################################################################################################
class DataBase: #데이터베이스 핸들링 클래스
    def __init__(self, kwd):
        self.kwd = kwd
    def handle_db_main(self, kwd):
        if type(kwd) == NoneType or len(kwd) == 0:
            pass
        elif type(kwd) != NoneType and len(kwd) >= 2:
            if kwd[0].isalpha() and kwd[1].isdigit() == True:
                cur.execute("SELECT * FROM 테이블 WHERE 스트롱넘버 = ?", ( (kwd[0]+kwd[1:].zfill(4) ).upper(), ) )
            else:
                cur.execute("SELECT * FROM 테이블 WHERE 표기1 = ? OR 표기2 = ? OR 표기3 = ?  OR 표기4 = ? OR \
                    의미1 LIKE ? OR 의미2 LIKE ? OR 의미3 LIKE ? OR 의미4 LIKE ? OR \
                    의미5 LIKE ? OR 의미6 LIKE ? OR 의미7 LIKE ?", \
                    (kwd, kwd, kwd, kwd, \
                    '%'+kwd+'%', '%'+kwd+'%', '%'+kwd+'%', '%'+kwd+'%', '%'+kwd+'%', '%'+kwd+'%', '%'+kwd+'%') )
        elif type(kwd) != NoneType and len(kwd) == 1:
            cur.execute("SELECT * FROM 테이블 WHERE 표기1 = ? OR 표기2 = ? OR 표기3 = ?  OR 표기4 = ? OR \
                의미1 LIKE ? OR 의미2 LIKE ? OR 의미3 LIKE ? OR 의미4 LIKE ? OR \
                의미5 LIKE ? OR 의미6 LIKE ? OR 의미7 LIKE ?", \
                (kwd, kwd, kwd, kwd, \
                '%'+kwd+'%', '%'+kwd+'%', '%'+kwd+'%', '%'+kwd+'%', '%'+kwd+'%', '%'+kwd+'%', '%'+kwd+'%') )
    def handle_db_rlt(self, fld, kwd):
        self.fld = fld
        if type(kwd) == NoneType or len(kwd) == 0:
            pass
        else:
            cur.execute("SELECT * FROM 테이블 WHERE "+fld+" = ?", (kwd, ) )

def find_words(input):
        DataBase(input).handle_db_main(input) # 데이터베이스 검색 함수(주)
        words = cur.fetchall() # 검색된 자료 불러오기
        return words

def find_origin(input):
    origin= [] # origin 자료를 위한 리스트 생성
    for i in range(len(input) ): # 검색한 단어의 '관련' 항에 기입된 'id'를 이용하여 추가검색
        org=(input[i][field_idx['관련1'] ], \
            input[i][field_idx['관련2'] ], \
            input[i][field_idx['관련3'] ], \
            input[i][field_idx['관련4'] ] )
        for j in range(4):
            DataBase(input).handle_db_rlt('id', org[j] )
            origin.extend(cur.fetchall() ) # 검색된 자료 불러오기
    return origin

def find_relate(keyword, input):
    field_rlt = (field[field_idx['관련1'] ], \
        field[field_idx['관련2'] ], \
        field[field_idx['관련3'] ], \
        field[field_idx['관련4'] ] ) # 데이터베이스 검색 함수를 위한 필드 정의
    relate = [] # relate 자료를 위한 리스트 생성
    for i in range(len(input) ): # '관련' 항에 검색한 단어의 'id'가 기록된 자료 검색
        for j in range(4):
            DataBase(keyword).handle_db_rlt(field_rlt[j], input[i][field_idx['id'] ] ) # 데이터베이스 검색 함수(관련)
            relate.extend(cur.fetchall() ) # 검색된 자료 불러오기
    return relate
    pass

# None -> '' 변환 함수
def rmv_none(input_data):
    for i in range(len(input_data) ):
        input_data[i] = list(input_data[i] )
        for j in range(0, 27):
            if input_data[i][j] == None:
                input_data[i][j] = ''

# def rmv_none(input_data):
#     return list(filter(lambda x: x != None, input_data))

# 중복 제거 함수
def rmv_dplct(input_data):
    mid_data = []
    for i in input_data:
        if i not in mid_data:
            mid_data.append(i)
    return mid_data

# 자료 갈무리 함수
def orgnz_data(input_data):
    return [[input_data[i][j] for j in tv_show] for i in range(len(input_data) ) ]

def mk_nx_node(input_data):
    for i in range(len(input_data) ):
        if input_data[i][field_idx['id'] ] in list(DG.nodes):
            continue
        else:
            text_node = input_data[i][field_idx['스트롱'] ]+'\n'+input_data[i][field_idx['표기1'] ]+'\n'+input_data[i][field_idx['id'] ]
            DG.add_node(input_data[i][field_idx['id'] ], text=text_node)

# def mk_nx_node(input_data):
#     for i in range(len(input_data) ):
#         DG.add_node(input_data[i][0], text=str(input_data[i][2]+'\n'+input_data[i][3] ) )

def mk_nx_edge(input_data):
    for i in range(len(input_data) ):
        for j in [field_idx['관련1'], field_idx['관련2'], field_idx['관련3'], field_idx['관련4']]:
            if input_data[i][j] != '':
                if input_data[i][j] in list(DG.nodes):
                    pass
                else:
                    node_temp = []
                    DataBase(input_data[i][j] ).handle_db_rlt('id', input_data[i][j] )
                    node_temp.extend(cur.fetchall() )
                    rmv_none(node_temp)
                    text_node = node_temp[0][field_idx['스트롱'] ]+'\n'+node_temp[0][field_idx['표기1'] ]+'\n'+node_temp[0][field_idx['id'] ]
                    DG.add_node(input_data[i][j], text=text_node)
                    node_temp = []
                DG.add_edge(input_data[i][j], input_data[i][0] )
            else:
                continue

# def mk_nx_edge(input_data):
#     for i in range(len(input_data) ):
#         for j in [15, 16, 17, 18]:
#             if input_data[i][j] != '':
#                 DG.add_edge(input_data[i][j], input_data[i][0] )
#             else:
#                 continue

# 트리뷰 생성 클래스
class TreeView_Ctrl:
    def __init__(self, tv):
        self.tv = tv
        for i in range(len(tv_column)+1):
            if i == 0:
                self.tv.column('#0', width=0, stretch=NO)
                self.tv.heading('#0', text='', anchor=CENTER)
            else:
                self.tv.column(tv_column[i-1], anchor=CENTER, width=tv_clm_len[i-1] )
                self.tv.heading(tv_column[i-1], text=field[tv_show[i-1] ], anchor=CENTER)
        pass
    pass

# 트리뷰 값(튜플) 클립보드에 복사 관련 함수들
def clip_tv_base(treeview):
    sel = treeview.selection()# 선택된 아이템들 획득
    root.clipboard_clear()# 클립보드 초기화
    # 헤더 복사
    headings = [treeview.heading('#{}'.format(i), 'text') for i in range(len(treeview.cget('columns') ) + 1) ]
    root.clipboard_append('\t'.join(headings) + '\n')
    for item in sel:
        # 열의 값들을 획득
        values = [treeview.item(item, 'text') ]
        values.extend(treeview.item(item, 'values') )
        # \t 으로 분리되도록 값들을 클립보드에 덧붙임
        root.clipboard_append('\t'.join(values) + '\n')
    pass

def clip_tv_1(event):
    clip_tv_base(tv_1)
def clip_tv_2(event):
    clip_tv_base(tv_2)
def clip_tv_3(event):
    clip_tv_base(tv_3)

####################################################################################################
# 버튼 클릭 명령 함수
####################################################################################################
def btncmd():
    #트리뷰 초기화
    for i in range(3):
        tv[i].delete(*tv[i].get_children() )

    #그래프 초기화
    plt.cla()
    #networkx 초기화
    DG.clear()

    #키워드 획득
    wrd = s_e.get() # 획득한 키워드를 wrd로 획득
    words = find_words(wrd)
    words.sort() # 불러온 자료 정렬

    origin = find_origin(words)
    origin.sort() # 불러온 자료 정렬

    relate = find_relate(wrd, words)
    relate.sort() # 불러온 자료 정렬

    rmv_none(words)
    rmv_none(origin)
    rmv_none(relate)

    origin = rmv_dplct(origin)
    relate = rmv_dplct(relate)

    origin = [i for i in origin if i not in words]
    relate = [i for i in relate if i not in words and i not in origin]

    words_show = []
    origin_show = []
    relate_show = []

    words_show = orgnz_data(words)
    origin_show = orgnz_data(origin)
    relate_show = orgnz_data(relate)

    for i in range(len(words_show) ):
        tv_1.insert(parent="", index=i, iid=i, text='', values=(words_show[i]) )
    for i in range(len(origin_show) ):
        tv_2.insert(parent='', index=i, iid=i, text='', values=origin_show[i] )
    for i in range(len(relate_show) ):
        tv_3.insert(parent='', index=i, iid=i, text='', values=relate_show[i] )

    mk_nx_node(words)
    mk_nx_node(origin)
    mk_nx_node(relate)
    mk_nx_edge(words)
    mk_nx_edge(relate)

    pos = nx.shell_layout(DG)
    nx.draw_networkx_nodes(DG, pos, node_size=2100, node_color='#00ff00')
    nx.draw_networkx_edges(DG, pos, node_size=2100)

    node_labels = nx.get_node_attributes(DG, 'text')
    nx.draw_networkx_labels(DG, pos, font_family='sans-serif', font_size=10, labels = node_labels)

    plt.show()

####################################################################################################
# 여기부터 프로그램 UI 관련 코드
####################################################################################################
root = Tk()# GUI 루프 시작
root.title('단어 검색')# 창 제목
# root.attributes('-fullscreen', True)
root.geometry('%dx%d+50+50' %(root.winfo_screenwidth()-100, root.winfo_screenheight()-200 ) )# 창 크기

# 프레임 셋업
frame_0 = Frame(root, relief='groove', bd=1, pady=14)# 검색창 프레임
frame_1 = Frame(root, relief='flat', bd=1, pady=14)# 검색 단어 출력 프레임
frame_2 = Frame(root, relief='flat', bd=1, pady=14)# 유래 출력 프레임
frame_3 = Frame(root, relief='flat', bd=1, pady=14)# 관련 단어 출력 프레임
frame = (frame_0, frame_1, frame_2, frame_3)

# 라벨 셋업
label_0 = Label(frame_0, text='검색할 단어를 입력하세요')# 검색창 라벨
label_1 = Label(frame_1, text='해당 단어')# 검색 단어 출력 라벨
label_2 = Label(frame_2, text='유래/관련 단어')# 유래 출력 라벨
label_3 = Label(frame_3, text='파생/관련 단어')# 관련 단어 출력 라벨
label = (label_0, label_1, label_2, label_3)

# 스크롤바/트리뷰 셋업
tvsb_v_1 = Scrollbar(frame_1, orient='vertical')# 트리뷰1용 세로 스크롤 바
tvsb_v_2 = Scrollbar(frame_2, orient='vertical')# 트리뷰2용 세로 스크롤 바
tvsb_v_3 = Scrollbar(frame_3, orient='vertical')# 트리뷰3용 세로 스크롤 바
tvsb_v = (tvsb_v_1, tvsb_v_2, tvsb_v_3)
tvsb_h_1 = Scrollbar(frame_1, orient='horizontal')# 트리뷰1용 가로 스크롤 바
tvsb_h_2 = Scrollbar(frame_2, orient='horizontal')# 트리뷰2용 가로 스크롤 바
tvsb_h_3 = Scrollbar(frame_3, orient='horizontal')# 트리뷰3용 가로 스크롤 바
tvsb_h = (tvsb_h_1, tvsb_h_2, tvsb_h_3)
tv_1 = Treeview(frame_1, height=7, xscrollcommand=tvsb_h_1.set, yscrollcommand=tvsb_v_1.set)# 검색 단어 출력 트리뷰
tv_2 = Treeview(frame_2, height=7, xscrollcommand=tvsb_h_2.set, yscrollcommand=tvsb_v_2.set)# 유래 출력 트리뷰
tv_3 = Treeview(frame_3, height=7, xscrollcommand=tvsb_h_3.set, yscrollcommand=tvsb_v_3.set)# 관련 단어 출력 트리뷰
tv = (tv_1, tv_2, tv_3)
for i in range(len(tv) ):
    tv[i]['columns']=tv_column

# 검색창
s_e = Entry(frame_0, width=14)
s_e.insert(0, "")#입력 가능

# 버튼
btn0 = Button(frame_0, padx=10, pady=5, text='검색', command=btncmd)

# 프레임/라벨 패킹
for i in range(len(frame) ):
    frame[i].pack()
    label[i].pack()

s_e.pack()# 엔트리(검색창) 패킹
btn0.pack()# 검색 버튼 패킹

# 스크롤바/트리뷰 패킹
for i in range(len(tv) ):
    tvsb_v[i].pack(side='right', fill='y')
    tvsb_v[i].config(command=tv[i].yview)
    tvsb_h[i].pack(side='bottom', fill='x')
    tvsb_h[i].config(command=tv[i].xview)
    TreeView_Ctrl(tv[i] )
    tv[i].pack(side='left', fill='y')

# <Control-c> 입력으로 선택 내용 클립보드 저장
tv_1.bind('<Control-c>', clip_tv_1)
tv_2.bind('<Control-c>', clip_tv_2)
tv_3.bind('<Control-c>', clip_tv_3)

root.mainloop()# GUI 루프 끝

con.close()# 데이터 베이스 닫기