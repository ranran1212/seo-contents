import streamlit as st
import openai

# Streamlitのフォームを設定
st.set_page_config(
    page_title="SEO記事構成案作成",
    page_icon="🐹",
    layout="wide"
)

with st.form("my_form"):
    api_key = st.text_input("OpenAI APIキーを入力してください", type="password")
    
    st.subheader("対策キーワードの入力（1〜3個）")
    keywords = [st.text_input(f"対策キーワード {i+1}") for i in range(3)]
    keywords = [k for k in keywords if k]  # 空の入力を除外
    
    st.subheader("競合記事の入力（3記事分）")
    articles = []
    for i in range(3):
        title = st.text_input(f"競合記事タイトル {i+1}")
        description = st.text_area(f"競合記事ディスクリプション {i+1}", height=100)
        if title and description:
            articles.append(f"{title}：{description}")
    
    # top_pの値をスライダーで選択
    st.subheader("設定")
    top_p_value = st.slider("top_pの値", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    st.caption("top_pは出力結果の多様性を制御する値で、0に近いほど一貫性が高く、1に近いほど多様性が増します")
    
    top_p_value = st.slider("出力結果の数", min_value=1, max_value=10, value=3, step=1)
    st.caption("出力する構成案の数を指定します")
    
    
    submit_button = st.form_submit_button("生成する")

if submit_button and api_key and articles:
    prompt = """SEO専門家として、競合記事よりも検索結果で上位に表示されるような記事の構成案を考えてください。
- 下記の情報を踏まえて、記事の構成案は①タイトル、②記事の概要、③オーディエンスの検索意図、④競合記事との差別化ポイント、⑤見出し（見出しの説明）の項目で作成すること。
- 明確なセクション分け、h2/h3見出しの設定すること。
- h2は3〜5個、h3は2〜4個で設定すること。
- 競合記事の情報を分析し、オーディエンスの検索意図・競合記事との差別化ポイントを設定すること。
- ガイドラインに従い作成すること。
- 対策キーワード見出しに適切に含めること。
- ターゲットオーディエンスにとって有益で、興味深い内容を提供すること。
- ビジネスライクなトーンとスタイルを維持すること。

## 対策キーワード
- {keyword1}
- {keyword2}
- {keyword3}

## 競合記事
- {article_title1}：{article_description1}
- {article_title2}：{article_description2}
- {article_title3}：{article_description3}

## ターゲットオーディエンス
- 大企業に所属する社会人
- 20代後半〜40代の中間管理職やマネージャークラス
- 所属企業のイベントに関わっている

## ガイドライン
- タイトルには必ず対策キーワードを含み、なるべく対策キーワードを前半に入れてください。
- 記事の概要には、この記事を読むことでどのような情報が得られるかを簡潔にまとめてください。
- それぞれの見出しには、どのようなコンテンツを書くべきかがわかる見出しの説明をつけてください。
- 記事コンテンツは2500文字〜3000文字を想定して、キーワードは1見出しに過剰に詰め込まず、自然な見出しを作成してください。
- 見出しの一番最後にはまとめ見出しを作成してください。まとめ見出しではH3見出しを作成する必要はありません。
- 有資格者や専門家の知見が必要な内容は含まないでください。
- 出力フォーマットで指定されている項目以外の内容を出力してはいけない。

## 出力フォーマット

### タイトル
### 記事の概要
### オーディエンスの検索意図
### 競合記事との差別化ポイント
### 見出し
- h2：
    - h2の説明：
- h3： 
    - h3の説明：
    """.format(
        keyword1=keywords[0], 
        keyword2=keywords[1] if len(keywords) > 1 else "", 
        keyword3=keywords[2] if len(keywords) > 2 else "", 
        article_title1=articles[0].split("：")[0], 
        article_description1=articles[0].split("：")[1],
        article_title2=articles[1].split("：")[0], 
        article_description2=articles[1].split("：")[1],
        article_title3=articles[2].split("：")[0], 
        article_description3=articles[2].split("：")[1]
    )
    
    for i in range(3):  
        # ChatGPT APIを呼び出し
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000,
            temperature=1,
            top_p=top_p_value,
            api_key=api_key
        )
        
        st.text_area(f"生成された記事の構成案{i+1}", response.choices[0].message['content'], height=500)