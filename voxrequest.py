import requests
import pprint

class vox:
    def __init__(self,address:str="http://localhost:50021"):
        """voicevoxに接続する。
        ボイスボックスに接続する。

        Args:
            address (str): url
        """
        self.address=address
        self.dict={}
        self.query={}
        self.speaker={}
    def audio_query(self,text:str,speaker:int):
        """合成用のクエリを作成。
        クエリの初期値を得ます。ここで得られたクエリはそのまま音声合成に利用できます。

        Args:
            text (str): 話す文章
            speaker (int): 喋る人(最適化)

        Returns:
            dict: クエリ
        """
        data = {}
        header = {
            'accept':'application/json'
        }
        param={
                'text':text,
                'speaker':speaker
        }
        req = requests.post(
            url=self.address+'/audio_query',
            json=data,
            headers=header,
            params=param
        )
        self.query=req.json()
    def synthesis(self,speaker:int):
        """音声合成する。
        クエリを基に音声合成を行います。

        Args:
            speaker (int): 喋る人(実際)

        Returns:
            bytes: wav音声
        """
        data = self.query
        header = {
            'accept':'application/wav',
            'Content-Type':'application/json'
        }
        param = {
            'speaker':speaker
        }
        req = requests.post(
            url=self.address+"/synthesis",
            json=data,
            headers=header,
            params=param
        )
        return req.content
    def speakers(self):
        """スピーカーid取得
        スピーカーのidと対応する名前（モード）を返します。
        """
        header = {
            'accept':'application/json'
        }
        req = requests.get(
            url=self.address+"/speakers",
            headers=header
        )
        self.speaker=req.json()
    def user_dict(self):
        """ユーザー辞書を取得
        ユーザー辞書に登録されている単語の一覧を返します。 単語の表層形(surface)は正規化済みの物を返します。

        Returns:
            dict: 辞書
        """
        header = {
            'accept':'application/json'
        }
        req = requests.get(
            url=self.address+"/user_dict",
            headers=header
        )
        self.dict=req.json()
    def user_dict_word(self,surface:str,pronunciation:str,accent_type:int,word_type:str='PROPER_NOUN',priority:int=0):
        """辞書に言葉を追加

        Args:
            surface (str): 変換する言葉（漢字・英語・日本語・キリル文字etc...)
            pronunciation (str): 読み方（カタカナ）
            accent_type (int): 先頭からどこをアクセントにするか（音が下がる場所）
            word_type (str, optional): [固有名詞(PROPER_NOUN)]、普通名詞(COMMON_NOUN)、動詞(VERB)、形容詞(ADJECTIVE)、語尾(SUFFIX)
            priority (int, optional): 優先度(デフォルト:0)。

        Returns:
            dict: 良し悪し
        """
        data = {}
        header = {
            'accept':'application/json'
        }
        param = {
            'surface':surface,
            'pronunciation':pronunciation,
            'accent_type':accent_type,
            'word_type':word_type,
            'priority':priority
        }
        req = requests.post(
            url=self.address+"/user_dict_word",
            json=data,
            headers=header,
            params=param
        )
        return req.content
    def user_dict_word_edit(self,word_uuid:str,surface:str=None,pronunciation:str=None,accent_type:int=None,word_type:str=None,priority:int=None):
        """辞書に言葉を編集

        Args:
            word_uuid (str): 単語のuuid
            surface (str): 変換する言葉（漢字・英語・日本語・キリル文字etc...)
            pronunciation (str): 読み方（カタカナ）
            accent_type (int): 先頭からどこをアクセントにするか（音が下がる場所）
            word_type (str, optional): [固有名詞(PROPER_NOUN)]、普通名詞(COMMON_NOUN)、動詞(VERB)、形容詞(ADJECTIVE)、語尾(SUFFIX)
            priority (int, optional): 優先度(デフォルト:0)。

        Returns:
            dict: 良し悪し
        """
        data = {}
        header = {
            'accept':'*/*'
        }
        param = {
            'surface':surface,
            'pronunciation':pronunciation,
            'accent_type':accent_type,
            'word_type':word_type,
            'priority':priority
        }
        req = requests.put(
            url=self.address+"/user_dict_word/"+word_uuid,
            json=data,
            headers=header,
            params=param
        )
        return req.content
    def user_dict_word_delete(self,word_uuid:str):
        """辞書の単語を消す

        Args:
            word_uuid (str): 消す単語のuuild

        Returns:
            bytes: 良し悪し
        """
        data = {}
        header = {
            'accept':'*/*'
        }
        param = {}
        req = requests.put(
            url=self.address+"/user_dict_word/"+word_uuid,
            json=data,
            headers=header,
            params=param
        )
        return req.content
    def show_dict(self):
        pprint.pprint(self.dict)
    def show_query(self):
        pprint.pprint(self.query)
    def show_speaker(self):
        pprint.pprint(self.speaker)
    def get_dict(self):
        return self.dict
    def get_query(self):
        return self.query
    def get_speakers(self):
        return self.speaker