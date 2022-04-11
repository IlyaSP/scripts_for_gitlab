import gitlab
from typing import Optional
import datetime
import os
import sys

def get_time_last_release(project_id: int, gl: gitlab.Gitlab) -> (str, Optional[str], Optional[str]):
    """
    Функция для получения даты последнего релиза в репозитории.
    """
    project = gl.projects.get(project_id)    # Получение данных о проекте
    release = project.releases.list()    # Получение списка всех релизов отсотрированных от новых к старым
    if len(release) != 0:
        timestring = release[0].released_at    # Получение временной метки создания последнего релиза
    else:
        timestring = 0
#    d = datetime.datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%S.%fZ")
    return timestring, project

def create_change_log(timestring, project):

    # Получение списка всех issues обновлённых после  timestring и имеющих статус closed
    if timestring != 0:
        issues = project.issues.list(updated_after=timestring, state='closed')
    else:
        issues = project.issues.list(state='closed')
    print(issues)
    with open("test.md", 'w', encoding='utf-8',) as f:
        f.write("CHANGELOG\n")
        for i in issues:
            f.write("- {0}\n".format(i.title))    # запись в файл наазваний issue

if __name__ == "__main__":
    try:
        gl = gitlab.Gitlab(os.getenv('CI_SERVER_URL'), private_token=os.getenv('GITLAB_TOKEN'), ssl_verify=False)
        gl.auth()
        print("=======CONNECT==========")
    except Exception as e:
        sys.exit(e)
    project_id = int(os.getenv('CI_PROJECT_ID'))    # id прокта для которого будут формироваться тэги
    timestring, project = get_time_last_release(project_id, gl)
    create_change_log(timestring, project)
