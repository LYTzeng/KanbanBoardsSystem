
# :construction_worker:開發中 KanbanBoardsSystem
An implementation of Kanban method based on Django web application.

~~很抱歉這其實不算是README 主要是讓組員更了解專案((希望(((被K><~~

## 測試方法
- 測試UAMS 
  ```bash
  專案路徑\KB> python -m unittest -v kanban\UAMS\test\uams_test.py -b
  ```
- 計算UAMS測試的Code coverage
  ```bash
  專案路徑\KB> coverage run --source=kanban\UAMS\src,kanban\UAMS\test -m unittest -v kanban\UAMS\test\uams_test.py -b
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
│  ├─PMS	專案管理子系統
│  ├─TMS	任務管理子系統
│  ├─UAMS	使用者管理子系統
│  │  ├─src
│  │  │  │  FirebaseAPIKey.py	API金匙，當然不在Github上
│  │  │  │  user.py		使用者管理子系統的Implementation
│  │  ├─test	測試
│  │  │  │  uams_test.py	單元測試
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
