# create_tag
Служит для формирования нового тэга после коммита, пуша или мердж реквеста. Формат тэга х.х.х. 
После того как скрипт отработает версия увеличится на единицу (1.0.0 -> 1.0.1). Более глобальная смена версий происходит с помощью
лэйбла при мерж реквесте (1.0.0 -> 1.2.0).

Снаружи скрипт получает имя ветки на базе которой будет сформирован тэг и путь по которому будет сохраняться файл VERSION в который помещается 
номер версии, который равен номеру сформированного тэга.

Serves to form a new tag after a commit, push or merge request. Tag format x.x.x. 3After the script runs, the version will increase by one (1.0.0 -> 1.0.1). A more global version change occurs with the help of a 4label during a merge request (1.0.0 -> 1.2.0).
Outside, the script receives the name of the branch on the basis of which the tag will be generated and the path along which the VERSION file will be saved 7in which the version number is placed, which is equal to generated tag number.

Пример применения
Application example
```
prepare_job:
  stage: prepare
  image: python:3.9.6-slim                                             
  script:
    - echo 'nameserver 8.8.8.8' > /etc/resolv.conf
    - apt-get -y update && apt-get -y install curl
    - pip3 install --upgrade python-gitlab
    - 'curl -k -H "PRIVATE-TOKEN: ${SERVICE_TOKEN}" "${CI_API_V4_URL}/projects/4/repository/files/create_tag%2Epy/raw?ref=main" > test1.py'
    - export PATH_FILE_VERSION=${PWD}/VERSION
    - export REF_NAME=main
    - python3 test1.py
```

# create_changelog_from_issues.py
Служит для формирования списка изменений в проекте на базе title закрытых issues с момента последнего релиза, если не было ни одного релиза, то в первый релиз попадут все закрытые issues.

Serves to generate a list of changes in the project based on the title of closed issues since the last release, if there was not a single release, then all closed issues will fall into the first release.
