"""
    Word_Searcher.pyw

    이 파일은 단어 검색 및 관계 시각화를 위한 Tkinter 기반 GUI 애플리케이션을 구현합니다.
    SQLite 데이터베이스와 상호작용하여 단어를 검색하고, 관련 단어와 파생 단어를 찾으며,
    그래프를 사용하여 단어 간의 관계를 시각화합니다.

    주요 클래스:
        - DatabaseHandler: SQLite 데이터베이스와의 상호작용을 처리합니다.
        - WordSearcher: 단어 검색 및 처리를 위한 메인 클래스입니다.
        - Application: 단어 검색을 위한 Tkinter 기반 GUI 애플리케이션입니다.
"""
import sqlite3
import re
import networkx as nx
from pyvis.network import Network
from tkinter import Tk, Frame, Label, Entry, Button, filedialog
from tkinter.scrolledtext import ScrolledText

FIELD = (
    'id', '언어', '스트롱 코드',
    '표기1', '표기2', '표기3', '표기4', '표기5', '표기6',
    '음역1', '음역2', '음역3', '음역4', '음역5', '음역6',
    '발음1', '발음2', '발음3', '발음4', '발음5', '발음6',
    '관련1', '관련2', '관련3', '관련4', '관련5', '관련6', '관련7',
    '의미1', '의미2', '의미3', '의미4', '의미5', '의미6', '의미7',
    '비고'
)# 데이터베이스 필드

FIELD_IDX = {
    'id': 0, '언어': 1, '스트롱': 2,
    '표기1': 3, '표기2': 4, '표기3': 5, '표기4': 6, '표기5': 7, '표기6': 8,
    '음역1': 9, '음역2': 10, '음역3': 11, '음역4': 12, '음역5': 13, '음역6': 14,
    '발음1': 15, '발음2': 16, '발음3': 17, '발음4': 18, '발음5': 19, '발음6': 20,
    '관련1': 21, '관련2': 22, '관련3': 23, '관련4': 24, '관련5': 25, '관련6': 26, '관련7': 27,
    '의미1': 28, '의미2': 29, '의미3': 30, '의미4': 31, '의미5': 32, '의미6': 33, '의미7': 34,
    '비고': 35
}# 데이터베이스 필드 인덱스

class DatabaseHandler:# 데이터베이스 핸들러
    """
        SQLite 데이터베이스와의 상호작용을 처리합니다.
    
        이 클래스는 쿼리를 실행하고 SQLite 데이터베이스와의 연결을 관리하는 메서드를 제공합니다.
    
        속성:
            connection (sqlite3.Connection): SQLite 데이터베이스에 대한 연결 객체.
            cursor (sqlite3.Cursor): SQL 쿼리를 실행하기 위한 커서 객체.
    
        메서드:
            execute_query(query, params=()): 선택적 매개변수와 함께 SQL 쿼리를 실행합니다.
            close(): 데이터베이스 연결을 닫습니다.
    
        예제:
            db_handler = DatabaseHandler('path_to_db.db')
            results = db_handler.execute_query('SELECT * FROM table_name WHERE column_name = ?', ('value',))
            db_handler.close()
    """
    def __init__(self, db_path):# 초기화
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=()):# 쿼리 실행
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):# 데이터베이스 연결 종료
        self.connection.close()

class WordSearcher:# 단어 검색기
    """
        단어 검색 및 처리를 위한 메인 클래스.
    
        이 클래스는 데이터베이스에서 단어를 검색하고, 관련 단어와 파생 단어를 찾으며,
        그래프를 사용하여 관계를 시각화하는 메서드를 제공합니다.
    
        속성:
            db_handler (DatabaseHandler): 쿼리를 실행하기 위한 데이터베이스 핸들러.
            graph (networkx.Graph): 단어 관계를 시각화하기 위한 그래프 객체.
    
        메서드:
            find_words(keyword): 주어진 키워드를 기반으로 데이터베이스에서 단어를 검색합니다.
            find_related(input): 입력된 단어와 관련된 단어를 찾습니다.
            find_derived(input): 입력된 단어에서 파생된 단어를 찾습니다.
            add_node(input_data): 입력 데이터를 기반으로 그래프에 노드를 추가합니다.
            add_edge(input_data): 입력 데이터를 기반으로 그래프에 엣지를 추가합니다.
            reformat_strong(words): 단어의 강한 번호를 재포맷합니다.
            nested_list_to_string(nested_list): 중첩된 리스트를 문자열로 변환합니다.
    """

    PRIME_PREP = (
        'G0001_0000', 'G0303_0000', 'G0473_0000',
        'G0575_0000', 'G0757_0000', 'G0846_0000',
        'G1223_0000', 'G1519_0000', 'G1537_0000',
        'G1722_0000', 'G1909_0000', 'G2095_0000',
        'G2596_0000', 'G3326_0000', 'G3844_0000',
        'G3956_0000', 'G4012_0000', 'G4253_0000',
        'G4314_0000', 'G4862_0000', 'G5259_0000'
        )# 주요 전치사
    QUERY_DERIVED = """
        SELECT * FROM 테이블
        WHERE 관련1 = ? OR 관련2 = ? OR 관련3 = ? OR 관련4 = ? OR 관련5 = ? OR 관련6 = ? OR 관련7 = ?
    """# 파생어 검색 쿼리

    def __init__(self, db_handler, graph):# 초기화 메서드
        self.db_handler = db_handler
        self.graph = graph if graph is not None else nx.Graph()

    def find_words(self, keyword):# 단어 검색 메서드
        results = []
        if keyword is None or len(keyword) == 0:
            pass
        elif len(keyword) > 1:
            if keyword[0].isalpha() and keyword[1:].isdigit():
                query, params = self._prepare_strong_query(keyword)
            else:
                query, params = self._prepare_general_query(keyword)
        elif len(keyword) == 1:
            query, params = self._prepare_general_query(keyword)
        
        if query and params:
            results = self.db_handler.execute_query(query, params)

        return sorted(results)

    def _prepare_strong_query(self, keyword):# 스트롱넘버 검색 쿼리 생성 메서드
        query = "SELECT * FROM 테이블 WHERE 스트롱넘버 = ?"
        formatted_keyword = (keyword[0] + keyword[1:].zfill(4)).upper()
        return query, (formatted_keyword,)

    def _prepare_general_query(self, keyword):# 일반 검색 쿼리 생성 메서드
        query = """
            SELECT * FROM 테이블
            WHERE 표기1 = ? OR 표기2 = ? OR 표기3 = ? OR 표기4 = ? OR 표기5 = ? OR 표기6 = ?
            OR 음역1 LIKE ? OR 음역2 LIKE ? OR 음역3 LIKE ?
            OR 음역4 LIKE ? OR 음역5 LIKE ? OR 음역6 LIKE ?
            OR 의미1 LIKE ? OR 의미2 LIKE ? OR 의미3 LIKE ?
            OR 의미4 LIKE ? OR 의미5 LIKE ? OR 의미6 LIKE ? OR 의미7 LIKE ?
        """
        params = [keyword] * 6 + [f"%{keyword}%"] * 13
        return query, params

    def find_related(self, input):# 관련어 검색 메서드
        query1 = """
            SELECT * FROM 테이블
            WHERE id = ?
        """
        related = set()

        while True:
            input_set = set(input)
            trigger = len(related)

            for item in input:
                rltds = (
                    item[FIELD_IDX['관련1'] ],
                    item[FIELD_IDX['관련2'] ],
                    item[FIELD_IDX['관련3'] ],
                    item[FIELD_IDX['관련4'] ],
                    item[FIELD_IDX['관련5'] ],
                    item[FIELD_IDX['관련6'] ],
                    item[FIELD_IDX['관련7'] ]
                )
                for rltd in rltds:
                    related.update(self.db_handler.execute_query(query1, (rltd,)))
                    input_set.update(related)

            input = list(input_set)
            
            if trigger == len(related):
                return sorted(input), sorted(list(related))

    def find_derived(self, input):# 파생어 검색 메서드
        derived = set()

        while True:
            input_set = set(input)
            trigger = len(derived)

            for item in input:
                if item[FIELD_IDX['id']] in self.PRIME_PREP:
                    continue
                params = (item[FIELD_IDX['id']],) * 7
                derived.update(self.db_handler.execute_query(self.QUERY_DERIVED, params))
                input_set.update(derived)

            input = list(input_set)
            
            if trigger == len(derived):
                return sorted(input), sorted(list(derived))

    def add_node(self, input_data):# networkx 노드 생성 메서드
        for item in input_data:
            node_id = item[FIELD_IDX['id']]
            if node_id not in self.graph.nodes:
                label, title = self._generate_node_label_and_title(item)
                self.graph.add_node(node_id, label=label, title=title, group=item[FIELD_IDX['언어']])

    def _generate_node_label_and_title(self, item):# 노드 레이블 및 타이틀 생성 메서드
        if item[FIELD_IDX['스트롱']] != '':
            label = item[FIELD_IDX['스트롱']]
            title = (
                f"◆언어: {item[FIELD_IDX['언어']]}\n"
                f"◆스트롱 색인 코드: {item[FIELD_IDX['스트롱']]}\n"
                f"▶▶▶표기◀◀◀\n"
                    f"{item[FIELD_IDX['표기1']]}\n{item[FIELD_IDX['표기2']]}\n{item[FIELD_IDX['표기3']]}\n"
                    f"{item[FIELD_IDX['표기4']]}\n{item[FIELD_IDX['표기5']]}\n{item[FIELD_IDX['표기6']]}\n"
                f"▶▶▶음역◀◀◀\n"
                    f"{item[FIELD_IDX['음역1']]}\n{item[FIELD_IDX['음역2']]}\n{item[FIELD_IDX['음역3']]}\n"
                    f"{item[FIELD_IDX['음역4']]}\n{item[FIELD_IDX['음역5']]}\n{item[FIELD_IDX['음역6']]}\n"
                f"▶▶▶번역◀◀◀\n"
                    f"ⓐ{item[FIELD_IDX['의미1']]}\nⓑ{item[FIELD_IDX['의미2']]}\n"
                    f"ⓒ{item[FIELD_IDX['의미3']]}\nⓓ{item[FIELD_IDX['의미4']]}\n"
                f"▶▶▶설명 및 용례◀◀◀\n"
                    f"{item[FIELD_IDX['비고']]}"
            )
        else:
            label = f"{item[FIELD_IDX['표기1']]}    {item[FIELD_IDX['표기2']]}    {item[FIELD_IDX['표기3']]}"
            title = (
                f"◆언어: {item[FIELD_IDX['언어']]}\n"
                f"▶▶▶표기◀◀◀\n"
                    f"{item[FIELD_IDX['표기1']]}\n{item[FIELD_IDX['표기2']]}\n{item[FIELD_IDX['표기3']]}\n"
                    f"{item[FIELD_IDX['표기4']]}\n{item[FIELD_IDX['표기5']]}\n{item[FIELD_IDX['표기6']]}\n"
                f"▶▶▶음역◀◀◀\n"
                    f"{item[FIELD_IDX['음역1']]}\n{item[FIELD_IDX['음역2']]}\n{item[FIELD_IDX['음역3']]}\n"
                    f"{item[FIELD_IDX['음역4']]}\n{item[FIELD_IDX['음역5']]}\n{item[FIELD_IDX['음역6']]}\n"
                f"▶▶▶번역◀◀◀\n"
                    f"ⓐ{item[FIELD_IDX['의미1']]}\nⓑ{item[FIELD_IDX['의미2']]}\n"
                    f"ⓒ{item[FIELD_IDX['의미3']]}\nⓓ{item[FIELD_IDX['의미4']]}\n"
                f"▶▶▶설명 및 용례◀◀◀\n"
                    f"{item[FIELD_IDX['비고']]}"
            )
        return label, title

    def add_edge(self, input_data):# networkx 엣지 생성 메서드
        while True:
            new_items = []

            for item in input_data:
                for i in [
                    FIELD_IDX['관련1'],
                    FIELD_IDX['관련2'],
                    FIELD_IDX['관련3'],
                    FIELD_IDX['관련4'],
                    FIELD_IDX['관련5'],
                    FIELD_IDX['관련6'],
                    FIELD_IDX['관련7']
                ]:
                    if item[i] != '':
                        if item[i] not in self.graph.nodes:
                            node_temp = []
                            node_temp.extend(self.db_handler.execute_query("SELECT * FROM 테이블 WHERE id = ?", (item[i],)))
                            node_temp = self._rmv_none(node_temp)
                            new_items.extend(node_temp)
                            self.add_node(node_temp)
                        else:
                            pass

                        if (item[i], item[0]) not in self.graph.edges:
                            self.graph.add_edge(item[i], item[0], arrows='none' )
                        else:
                            pass

            if new_items == []:
                break

            input_data.extend(new_items)

    def _rmv_none(self, data):# None 값 제거 메서드
        return [[item if item is not None else '' for item in row] for row in data]
    
    def reformat_strong(self, words):# 스트롱 코드 형식 변경 메서드
        for word in words:
            word[FIELD_IDX['스트롱'] ] = re.sub(r'([a-zA-Z])0+(\d+)', r'\1\2', word[FIELD_IDX['스트롱'] ])
        return words

    @staticmethod
    def nested_list_to_string(nested_list):# 중첩 리스트를 문자열로 변환하는 메서드
        result = []

        if isinstance(nested_list[0], list):
            for i, sublist in enumerate(nested_list):
                if i > 0:
                    result.append("\n\n▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶▶\n\n")# 구분선 추가

                for j, item in enumerate(sublist):
                    if j > 0:
                        result.append("\n")
                    result.append(str(item))
        else:
            for i, item in enumerate(nested_list):
                if i > 0:
                    result.append("\n")
                result.append(str(item))

        return "".join(result)

class Application:# 어플리케이션 클래스
    """
        단어 검색을 위한 Tkinter 기반 GUI 애플리케이션.
    
        이 클래스는 데이터베이스에서 단어를 검색하고, 검색 결과를 표시하며,
        그래프를 사용하여 단어 간의 관계를 시각화하는 그래픽 사용자 인터페이스(GUI)를 제공합니다.
    
        속성:
            root (Tk): Tkinter 애플리케이션의 루트 윈도우.
            word_searcher (WordSearcher): 검색 쿼리를 실행하기 위한 단어 검색 객체.
            graph (networkx.Graph): 단어 관계를 시각화하기 위한 그래프 객체.
            last_directory (str): 결과를 저장하는 데 사용된 마지막 디렉토리.
            search_entry (Entry): 검색 키워드를 입력하기 위한 입력 위젯.
            result_text (ScrolledText): 검색 결과를 표시하기 위한 텍스트 위젯.
    
        메서드:
            setup_ui(): 사용자 인터페이스 구성 요소를 설정합니다.
            search_command(): 검색 명령을 실행하고 결과를 표시합니다.
    """
    def __init__(self, root, word_searcher):# GUI 초기화
        self.root = root
        self.word_searcher = word_searcher
        self.graph = word_searcher.graph
        self.last_directory = '.'
        self.setup_ui()

    def setup_ui(self):# GUI 구성 메서드
        self.root.title("단어 검색기")
        self.root.state("zoomed")
        self.root.configure(bg="black")

        frame_0 = Frame(self.root, relief='groove', bd=1, pady=7, bg="#100c08")
        frame_1 = Frame(self.root, relief='flat', bd=1, pady=7, bg="black")
        
        frame_0.pack()
        frame_1.pack(fill="both", expand=True)

        label_0 = Label(frame_0, text='검색할 단어를 입력하세요', bg="#100c08", fg="white")
        label_1 = Label(frame_1, text='검색 결과', bg="black", fg="white")
        
        label_0.pack()
        label_1.pack()

        self.search_entry = Entry(frame_0, width=14)
        self.search_entry.pack()

        Button(frame_0, text='검색', command=self.search_command).pack()

        self.result_text = ScrolledText(frame_1, padx=3, pady=3, bg="#100c08", fg="white")
        self.result_text.pack(fill="both", expand=True)

    def search_command(self):# 검색 명령 메서드
        self.dscrpt_show = (
            FIELD_IDX['언어'], FIELD_IDX['스트롱'],
            FIELD_IDX['표기1'], FIELD_IDX['표기2'], FIELD_IDX['표기3'],
            FIELD_IDX['표기4'], FIELD_IDX['표기5'], FIELD_IDX['표기6'],
            FIELD_IDX['음역1'], FIELD_IDX['음역2'], FIELD_IDX['음역3'],
            FIELD_IDX['음역4'], FIELD_IDX['음역5'], FIELD_IDX['음역6'],
            FIELD_IDX['의미1'], FIELD_IDX['의미2'], FIELD_IDX['의미3'],
            FIELD_IDX['의미4'], FIELD_IDX['의미5'], FIELD_IDX['의미6'], FIELD_IDX['의미7'],
            FIELD_IDX['비고']
        )# 표시할 필드 설정

        self.color_map = {
            '히브리어/아람어': 'gold',
            '헬라어': 'aqua',
            '라틴어': '#9f0807',
            '영어': 'violet'
        }# 언어별 색상 설정

        self.graph.clear()

        keyword = self.search_entry.get()
        words = self.word_searcher.find_words(keyword)

        words_temp, related = self.word_searcher.find_related(words)
        words_temp, derived = self.word_searcher.find_derived(words_temp)

        words = self.word_searcher._rmv_none(words)
        related = self.word_searcher._rmv_none(related)
        derived = self.word_searcher._rmv_none(derived)

        related = [item for item in related if item not in words]
        derived = [item for item in derived if item not in words and item not in related]

        words = self.word_searcher.reformat_strong(words)
        related = self.word_searcher.reformat_strong(related)
        derived = self.word_searcher.reformat_strong(derived)

        self.dscrpt_words = [[row[i] for i in self.dscrpt_show] for row in words]

        self.result_text.configure(state="normal")
        self.result_text.delete(1.0, "end")
        self.result_text.insert("1.0", self.word_searcher.nested_list_to_string(self.dscrpt_words))
        self.result_text.configure(state="disabled")

        self.word_searcher.add_node(words + related + derived)
        self.word_searcher.add_edge(words + related + derived)

        net = Network(bgcolor='black', font_color='white', notebook=False, directed=False)
        net.from_nx(self.graph)

        default_color = '#c0c0c0'

        for node in net.nodes:
            group = node['group']
            node['color'] = self.color_map.get(group, default_color)

        for edge in net.edges:
            edge['color'] = '#808080'

        directory = filedialog.askdirectory\
            (title= '결과를 저장할 폴더를 선택해 주세요.', initialdir= self.last_directory)

        net.toggle_physics(True)
        net.show_buttons(filter_=['physics'])
        net.show(directory+'/'+str(keyword)+f".html", notebook=False)

if __name__ == "__main__":# 메인 함수
    db_path = "./bbwdb.db"
    db_handler = DatabaseHandler(db_path)
    graph = nx.Graph()

    word_searcher = WordSearcher(db_handler, graph)

    root = Tk()
    app = Application(root, word_searcher)
    root.mainloop()

    db_handler.close()