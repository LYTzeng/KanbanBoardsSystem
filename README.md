
# :construction_worker:開發中 KanbanBoardsSystem
An implementation of Kanban method based on Django web application.

~~很抱歉這其實不算是README 主要是讓組員更了解專案((希望(((被K><~~

## 測試方法
- 單元測試 
  ```bash
  專案路徑\KB> python -m unittest -v kanban\testing\pms_test.py -b
  專案路徑\KB> python -m unittest -v kanban\testing\uams_test.py -b
  專案路徑\KB> python -m unittest -v kanban\testing\tms_test.py -b
  ```
- 計算測試的Code coverage
 
  pip 先
  
  ```bash
  pip install coverage
  ```
 
  再用!
  
  ```bash
  專案路徑\KB> coverage run --source=kanban\UAMS\src,kanban\testing -m unittest -v kanban\testing\uams_test.py -b
  專案路徑\KB> coverage report -m
  專案路徑\KB> htmlcov\index.html
  ```

## 專案架構
```text
│  manage.py
│  requirements.txt	條列專案依賴的package
├─kanban	專案主要程式碼
│  │  admin.py	本專案不會用到
│  │  models.py	本專案不會用到
│  │  tests.py	本專案不會用到
│  │  views.py	就是MVC中的View
│  ├─firebase
│  │  │  FirebaseAPIKey.py 這個是API密匙
│  │  │  setup.py 用來連資料庫的Class
│  ├─PMS	專案管理子系統
│  │  ├─src
│  │  │  │  project.py
│  ├─TMS	任務管理子系統
│  ├─UAMS	使用者管理子系統
│  │  ├─src
│  │  │  │  user.py
│  ├─testing 測試和測資放這
│  │  │  mock.py
│  │  │  pms_test.py
│  │  │  uams_test.py
├─KB	主要是Django框架會用到的必要設定
│  │  settings.py	環境變數
│  │  urls.py		定義URL對應被呼叫的View
│  │  wsgi.py		wsgi server
├─static	放靜態檔 如圖片、JS、CSS等
│  ├─css
│  │  └─jqwidgets	jqwidgets的配色 用在看板色彩主題
│  │      └─styles
│  │          │  jqx.base.css
│  │          │  jqx.light.css
│  │          │
│  │          └─images
│  │                  圖片
│  ├─js		放JS第一層目錄的都是現成的框架
│  │  │  d3-scale-chromatic.v1.min.js
│  │  │  d3.v4.min.js
│  │  │  jquery-1.12.4.min.js
│  │  │  jquery.lazy.min.js
│  │  │  jquery.lazy.plugins.min.js
│  │  │  uikit-icons.min.js
│  │  │  uikit.min.js
│  │  └─kb	這邊放自己寫的JS
│  │          basic-board.js	看板頁面的JS
│  └─media
│          favicon.png
│          favicon.svg
└─templates	Django Template 就是前端的HTML和模板語言
    │  board.html
    │  settings.html
    │  sign_up.html
    ├─basic
    │      basic.html	模板基底，所有頁面共通使用
    └─css
        └─kb
```

  
---
###### README.MD使用[stackedit](https://stackedit.io/)製作
###### ©2018 by Li Yen Tseng
