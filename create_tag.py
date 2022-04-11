import gitlab
import os
import sys
import subprocess
import logging
from typing import Optional

#FORMAT = '{asctime} | booking_manager | {module} | {levelname} | {message}'
#logging.basicConfig(format=FORMAT)
#logger = logging.getLogger("ver_bumper")

def get_last_tag(project_id: int, cur_commit_sha: str, gl: gitlab.Gitlab) -> (str, Optional[str], Optional[str]):
    """
    Функция для получения последнего тэга в репозитории. Так же здесь проверяется был ли это мерж реквест или нет,
    если да, то из него извлекается лэйбл
    """
    label = None
    project = gl.projects.get(project_id) 
    tags = project.tags.list()    # список всех тэгов для проекта, упорядоченных по дате изменения
    mrs = project.mergerequests.list(order_by='updated_at')    # спосок мердж реквестов для проекта, упорядоченных по дате изменения
    if len(mrs) > 0:
        for i in mrs:
            if i.merge_commit_sha == cur_commit_sha:
                if len(i.labels) !=0:
                   label = i.labels[0]
                else:
                    label = None
                break    
            else:
                continue
    else:
        print("no merge request")            
    print(label)

    if len(tags) == 0:
        last_tag = '0.0.0'
    else:
        last_tag = tags[0].name
        last_commit_sha=tags[0].commit.get('id')
    return last_tag, last_commit_sha, label


def form_new_tag(project_id: int, cur_commit_sha: str, gl: gitlab.Gitlab) -> str:
    """
    Функция для формирования нового тэга. Если в мердж реквесте есть лэбл, то новый тэг будет равен лэйблу.
    """
    last_tag, last_commit_sha, label = get_last_tag (project_id, cur_commit_sha, gl)
    print(" last_tag = {0}\n last commit sha = {1}\n merge label = {2}\n current commit sha ={3}".format(last_tag, last_commit_sha, label, cur_commit_sha))
    if last_commit_sha == cur_commit_sha:
        # если хэш последнего комита равен текущему хэшу, то считаем, что изменений не было, новый тэг не нужен.
        print("==== no changes =====")
        sys.exit("3")
    else:
        if label != None:
            new_tag = label
        else:
            if last_tag == "0.0.0":
                new_tag = "1.0.0"
            else:
                last_tag_separate = last_tag.split('.')
                new_tag = ("{0}.{1}.{2}".format(last_tag_separate[0],last_tag_separate[1], int(last_tag_separate[2])+1))
            if last_tag == "0.0.0":
                new_tag = "1.0.0"
            else:
                last_tag_separate = last_tag.split('.')
                new_tag = ("{0}.{1}.{2}".format(last_tag_separate[0],last_tag_separate[1], int(last_tag_separate[2])+1))
    return new_tag


def create_new_tag(new_tag: str, project_id: int, ref_name: str):
    project = gl.projects.get(project_id)
    try:
        project.tags.create({'tag_name': new_tag, 'ref': ref_name})
        path_file_ver = os.getenv('PATH_FILE_VERSION')
        subprocess.run('echo "$VERSION" > "$PATH_FILE_VERSION"', shell=True, env={'VERSION': new_tag, 'PATH_FILE_VERSION': path_file_ver})
        print("new tag {0} in ref {1} was creted".format(new_tag, ref_name))
    except Exception as e:
        sys.exit(e)


if __name__ == "__main__":
    try:
        gl = gitlab.Gitlab(os.getenv('CI_SERVER_URL'), private_token=os.getenv('GITLAB_TOKEN'), ssl_verify=False)
        gl.auth()
        print("=======CONNECT==========")
    except Exception as e:
        sys.exit(e)
    ref_name = os.getenv('REF_NAME')    # название ветки, на базе которой создаём тэг
    project_id = int(os.getenv('CI_PROJECT_ID'))    # id прокта для которого будут формироваться тэги
    cur_commit_sha = os.getenv('CI_COMMIT_SHA')    # хэш текущего комита
    new_tag = form_new_tag(project_id, cur_commit_sha, gl)
    create_new_tag(new_tag, project_id, ref_name)

