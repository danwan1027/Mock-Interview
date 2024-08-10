# Monk Interview

## 如何開始

### 1. clone 下來
```
git clone https://github.com/danwan1027/Mock-Interview.git
```

### 2. 去line裡面下載instance資料夾
放在MOCK-INTERVIEW底下(不是小的那個)

### 3. 建立虛擬環境(非必要)
不一定要用，避免套件跟本機環境打架而已
mac的指令我沒測過
* 建立虛擬環境(名字取.venv才會被gitignore)
    ```
    // Windows
    python -m venv .venv
    // mac
    python3 -m venv .venv
    ```
* 進入虛擬環境
    ```
    // Windows
    .venv\Scripts\activate
    // mac
    . .venv/bin/activate
    ```
* 離開虛擬環境
    ```
    deactivate
    ```
* vscode右下角好像也可以進行上面的操作
![image](https://i.imgur.com/whIbRj7.png)
> 你們弄到這裡架構應該會跟這裡一樣

### 4. 下載相關套件
進到MOCK-INTERVIEW(不是小的那個)
```
npm install
npm install @heygen/streaming-avatar
pip install -r requirements.txt
```
進到 Client 資料夾
```
npm install react-router-dom
```

### 5. Get HEYGEN API Key
到 https://app.heygen.com/settings?nav=API 申請一個 Trail Token，貼到 Server/.env 裡面
```
HEYGEN_API_KEY=YOUR_API_KEY
```

### 6. 啟動
到根目錄執行
```
npm start
```



## 架構
### 新的架構更動
這個 project 現在分成前端 React ，後端 Flask，後端的部分我直接把之前的整包都丟到 Server folder 裡面

每一次執行 npm start，系統就會自動執行開始後端的 python run.py 和 開始前端的 npm start

前端是 3000 port，後端是 3001 port，之後有需要傳資料的話要使用 API 傳


### 架構簡介
這個project用了MTV架構，MTV是MVC的一個變種，總之兩個類似，MTV分別代表:
* __Model__: 和MVC的Model一樣，處理與資料相關的所有事務(如何存取、如何確認有效性、包含哪些行為以及資料之間的關係等)。
* __Template__: html那些東西。
* __View__: 處理業務邏輯、封裝結果的部分，負責處理 URL 與 callback 函式之間的關係，每一個view都代表一個簡單的Python function。
![image](https://i.imgur.com/61uiMm8.png)

### 資料夾和檔案介紹

| 名字     |    作用 |
| :-----: | :-----: |
| run.py   |   用來啟動(沒意外應該不用動)   |
| requirements.txt   |   所有要pip install的東西都寫這裡(最好加上版本)   |
| config/development.py   |   開發環境的配置   |
| config/production.py   |   正式環境的配置   |
| instance/config.py   |   資料庫私鑰之類不可上傳的東西   |
| mock_interview/__init __.py   |   把環境配置還有mock_interview所有的東西整合初始化   |
| mock_interview/models/   |   就是各個model   |
| mock_interview/models/__init __.py   |  整合model    |
| mock_interview/static/   |   放css, js, 圖片的地方   |
| mock_interview/templates/   |   html那些東西放這裡(可以用Jinja2，應該類似thymeleaf)   |
| mock_interview/views/   |   各個view(原本的router拆開而已)   |
| mock_interview/views/__init __.py   |   整合view   |

## 新增自己的model或view
### model
直接在models資料夾裡面新增你的model就可以開始寫了，不用額外設定
### view
這個比較麻煩一點，一樣先在views資料夾底下新增你的view，以home為例:
1. 在mock_interview/views/裡面新增一個home.py
    * 特別注意blueprint的部分，它是用來管理各個view的，每個view有一個blueprint，最後要註冊到__init __.py裡面
    * <yourblueprint>表示你自己取的blueprint的名字，我建議跟檔名一樣
    ```python
    from flask import Blueprint, render_template # 記得inport Blueprint

    # 宣告blueprint  
    # <yourblueprint> = Blueprint(' <yourblueprint>', __name__)
    home = Blueprint('home', __name__)  

    @home.route('/')  # <yourblueprint>.route()
    def index():
        return render_template('index.html')
    ```
2.  修改**mock_interview/views/__init __.py**
    ```python
    from flask import Blueprint

    # blueprint in views
    # 在這裡import前面弄的blueprint
    from .home import home
    
    def init_views(app):
        # 在這裡註冊前面弄的blueprint
        # app.register_blueprint(<yourbluepeint>)
        app.register_blueprint(home)
        
    ```
## 面試功能相關function
**面試開始**
  **mock_interview/views/interview.py - 第20行**

``` @interview.route('/start_camera')
    def start_camera():
        global cap
        cap = cv2.VideoCapture(0)
        
        #########################
        #冠程在這裡串出去你的function
        #########################
        
        return 'Camera started'
```
**面試結束**
  **mock_interview/views/interview.py - 第26行**

``` 
    @interview.route('/end_interview')
    def end_interview():
        global cap, total_emotion_count, angry_count, disgust_count, fear_count, happy_count, sad_count, surprise_count, neutral_count, total_frames, looking_at_camera_frames
        if cap:
            cap.release()
            cap = None
    
        # Calculate percentages
        stats = {
            'total_emotion_count': total_emotion_count,
            'angry_percent': round(angry_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
            'disgust_percent': round(disgust_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
            'fear_percent': round(fear_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
            'happy_percent': round(happy_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
            'sad_percent': round(sad_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
            'surprise_percent': round(surprise_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
            'neutral_percent': round(neutral_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
            'percentage_looking_at_camera': round(looking_at_camera_frames / total_frames * 100) if total_frames > 0 else 0
        }
        
        ##################################################
        #維綸要在這裡拿圖像辨識參數
        #參數包含：
        #總共偵測幾次情緒 total_emotion_count
        #六種情緒比例 angry_percent,disgust_percent,fear_percent,happy_percent,sad_percent,surprise_percent,neutral_percent
        #眼睛看鏡頭/不看鏡頭的時間比例 percentage_looking_at_camera
        #################################################


        # Reset counters
        total_emotion_count, angry_count, disgust_count, fear_count, happy_count, sad_count, surprise_count, neutral_count = (0, 0, 0, 0, 0, 0, 0, 0)
        total_frames = 0
        looking_at_camera_frames = 0

    return jsonify(stats)
```
