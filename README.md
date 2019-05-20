
# KanbanBoardsSystem
![course proj](https://img.shields.io/badge/course%20project-2018%20%E8%BB%9F%E5%B7%A5-green.svg?style=flat-square)
![contributers](https://img.shields.io/github/contributors/LYTzeng/KanbanBoardsSystem.svg?style=flat-square)
![django version](https://img.shields.io/badge/version-1.8.19-blue.svg?style=flat-square&logo=django)
![pytohn versions](https://img.shields.io/pypi/pyversions/django.svg?style=flat-square)
<a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangomade124x25.gif" border="0" alt="Made with Django." title="Made with Django." /></a>
![Inactive](https://img.shields.io/badge/repo%20status-inactive-yellowgreen.svg?style=flat-square)
\
An implementation of Kanban method based on Django web application.

~~很抱歉這其實不算是README 主要是讓組員更了解專案((希望(((被K><~~
## 注意事項
  如果需要執行專案，請先開通GCP的firebase，將API key以Dictionary的形式放入`kanban\firebase\FirebaseAPIKey.py`中
  `FirebaseAPIKey.py`中會有一個get() function回傳API Key 的Dictionary型別資料
  
  另外需要Firebase credentials，是一個JSON檔，將其路徑貼在`kanban\firebase\setup.py`中的第13行
  詳細自己看吧 <https://firebase.google.com/docs/admin/setup>
  

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
│  │  └─src
│  │      │  task.py
│  ├─UAMS	使用者管理子系統
│  │  ├─src
│  │  │  │  collection.py
│  │  │  │  user.py
│  ├─testing 測試和測資放這
│  │  │  mock.py
│  │  │  pms_test.py
│  │  │  tms_test.py
│  │  │  uams_test.py
├─KB	主要是Django框架會用到的必要設定
│  │  settings.py	環境變數
│  │  urls.py		定義URL對應被呼叫的View
│  │  wsgi.py		wsgi server
├─static	放靜態檔 如圖片、JS、CSS等
│  ├─css
│  │  ├─jqwidgets	jqwidgets的配色 用在看板色彩主題
│  │  │   └─styles
│  │  │       │  jqx.base.css
│  │  │       │  jqx.light.css
│  │  │       │
│  │  │       └─images
│  │  │               圖片
│  │  └─kb 自己寫的CSS   
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
    │  create_card.html
    │  create_project.html
    │  index.html
    │  login.html
    │  navbar.html
    │  settings.html
    │  sign_up.html
    └─basic
        └─basic.html	模板基底，所有頁面共通使用
```

  
---
###### README.MD使用[stackedit](https://stackedit.io/)製作
###### ©2018 by Li Yen Tseng
