"""任務管理子系統
任務新增/刪除要連動Project.add_task()和Project.del_task()
"""
import time
from datetime import datetime


class Task:
    def __init__(self, Firebase, project_id: str):
        self.project_id = project_id
        self.firebase = Firebase
        self.project_collection = self.firebase.firestore().collection('projects')
        self.task_collection = self.project_collection.document(self.project_id).collection('tasks')
        self.task_document = None
        self.task_id = None     # type: str # 任務ID
        self.content = None     # type: str # 任務內容
        self.owner = None       # type: str # 任務負責人
        self.start_time = None  # type: time.time()  # 任務發起時間
        self.end_time = None    # type: time.time() # 任務結束時間(移到done欄時紀錄)
        self.start_progress = None  # type: time.time() # 移到progress欄時開始紀錄
        self.end_progress = None    # type: time.time() # 移出progress欄時紀錄的時間點
        self.working_time = None    # type: datetime.second # start_progress減去end_progress 每次會累加
        self.color = None       # type: str # 顏色

    '''add and delete'''
    def add_task(self, request):
        """建立任務 包含 任務內容、管理員、卡片顏色、卡片建立日期"""
        ref = self.task_collection.document()
        self.task_id = ref.id
        self.content = request.POST.get('content')
        self.owner = request.POST.get('owner')
        self.color = request.POST.get('color')
        self.start_time = time.time()  # 這裡用的時間是 Unix timestamp 格式
        data = {
            'content': self.content,
            'owner': self.owner,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'start_progress': self.start_progress,
            'end_progress': self.end_progress,
            'working_time': self.working_time,
            'color': self.color
        }
        self.task_collection.document(self.task_id).set(data)
        self.task_document = self.task_collection.document(self.task_id)

    def del_task(self):
        """刪除任務 並重新初始化Class"""
        self.task_document.delete()
        self.__init__(self.firebase, self.project_id)

    '''update'''
    def update(self, request):
        """使用者變更卡片內容後，會呼叫這裡"""
        self.content = request.POST.get('content')
        self.owner = request.POST.get('owner')
        self.color = request.POST.get('color')
        self.task_document.update({'content': self.content})
        self.task_document.update({'owner': self.owner})
        self.task_document.update({'color': self.color})

    def set_end_time(self):
        """當卡片移至done 會記錄"""
        self.end_time = time.time()
        self.task_document.update({'end_time': self.end_time})

    def set_start_progress(self):
        """當卡片從任一處 移動到progress時 會開始記錄"""
        self.start_progress = time.time()
        self.task_document.update({'start_progress': self.start_progress})

    def set_end_progress(self):
        """當卡片移出progress 會記錄的時間點
        同時計算累加工時"""
        if self.start_progress is not None:
            self.end_progress = time.time()
            self.task_document.update({'end_progress': self.end_progress})
            dt_start = datetime.fromtimestamp(self.start_progress)
            dt_end = datetime.fromtimestamp(self.end_progress)
            dt_duration = dt_end - dt_start
            duration_sec = dt_duration.seconds
            self.working_time = self.refresh(self.task_id)['working_time']
            self.task_document.update({'working_time': duration_sec + self.working_time})  # 累加

    '''read'''
    def get(self, request=None, task_id: str = str()):
        """
        如果不是要Add task，而是要讀取現有的Task 會使用這個
        :param request: django request
        :param task_id: 若不使用request 也可用字串代替task id
        :return: dict 是任務完整的資訊，就是refresh()的回傳值
        """
        if request is not None:
            self.task_id = request.POST.get('taskId')
            data = self.refresh(self.task_id)
            return data
        elif task_id != str():
            self.task_id = task_id
        else:
            data = self.refresh(self.task_id)
            return data
        data = self.refresh(task_id)
        return data

    def refresh(self, task_id: str):
        """
        刷新Class的狀態 和資料庫同步
        :param task_id:
        :return: 是任務完整的資訊 字典可轉成JSON傳送
        """
        self.task_id = task_id
        self.task_document = self.task_collection.document(self.task_id)
        data = self.task_document.get()
        if data.exists == False: return FileNotFoundError  # 任務不存在的意外處理
        data = data.to_dict()
        self.content = data['content']
        self.owner = data['owner']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.start_progress = data['start_progress']
        self.end_progress = data['end_progress']
        self.working_time = data['working_time']
        self.color = data['color']
        return data