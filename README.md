# Monk Interview

## 如何開始

### 1. clone 下來
```
git clone https://github.com/danwan1027/Mock-Interview.git
```

### 2. 去line裡面下載instance資料夾
放在MONK-INTERVIEW底下(不是小的那個)

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
![image](https://hackmd.io/_uploads/HJclOe1DC.png)
> 你們弄到這裡架構應該會跟這裡一樣

### 4. 下載相關套件
進到MONK-INTERVIEW(不是小的那個)
```
pip install -r requirements.txt
```

### 5. 啟動
```
python run.py
```



## 架構

### 架構簡介
這個project用了MTV架構，MTV是MVC的一個變種，總之兩個類似，MTV分別代表:
* __Model__: 和MVC的Model一樣，處理與資料相關的所有事務(如何存取、如何確認有效性、包含哪些行為以及資料之間的關係等)。
* __Template__: html那些東西。
* __View__: 處理業務邏輯、封裝結果的部分，負責處理 URL 與 callback 函式之間的關係，每一個view都代表一個簡單的Python function。
![image](https://hackmd.io/_uploads/Bktkcg1DA.png)

### 資料夾和檔案介紹

| 名字     |    作用 |
| :-----: | :-----: |
| run.py   |   用來啟動(沒意外應該不用動)   |
| requirements.txt   |   所有要pip install的東西都寫這裡(最好加上版本)   |
| config/development.py   |   開發環境的配置   |
| config/production.py   |   正式環境的配置   |
| instance/config.py   |   資料庫私鑰之類不可上傳的東西   |
| monk_interview/__init __.py   |   把環境配置還有monk_interview所有的東西整合初始化   |
| monk_interview/models/   |   就是各個model   |
| monk_interview/models/__init __.py   |  整合model    |
| monk_interview/static/   |   放css, js, 圖片的地方   |
| monk_interview/templates/   |   html那些東西放這裡(可以用Jinja2，應該類似thymeleaf)   |
| monk_interview/views/   |   各個view(原本的router拆開而已)   |
| monk_interview/views/__init __.py   |   整合view   |

## 新增自己的model或view
### model
直接在models資料夾裡面新增你的model就可以開始寫了，不用額外設定
### view
這個比較麻煩一點，一樣先在views資料夾底下新增你的view，以home為例:
1. 在monk_interview/views/裡面新增一個home.py
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
2.  修改**monk_interview/views/__init __.py**
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