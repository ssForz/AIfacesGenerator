# AIfacesGenerator
### Презентация
Презентация в файле AIfaces_pres.pdf

### Архитектура проекта на стадии планирования:
![image](https://github.com/user-attachments/assets/bb07e0db-d4d2-493b-b673-9cc62dce606d)

* В результате архитектура была реализована без сервиса cloud.ru

Замечание: При обучении возникла проблема: перед подготовкой к сдаче слетела полностью система Ubuntu, на которой была натренирована модель ~70 эпох, поэтому в спешке было вновь осуществлено только 30 эпох (к сожалению в моменте готовая модель была только на одном компьютере). В связи с этим качество результатов генерации сильно не дотягивает до желаемого(

Оригинальный репозиторий с нейронкой https://github.com/0x5eba/Anime-Character-Generator.git

Обучаем сами (директория с данными и сгенерированная модель отсутствуют в репозитории из-за веса. Гайд по обучению и всему что связано с нейросетью в директории network или по ссылке на оригинальный гитхаб)


### Запуск
Запуск проекта
```
docker-compose build
docker-compose up -d rabbit_mq
docker-compose up -d bot
docker-compose up -d app
```

Либо
```
docker-compose up --build
```
### Результаты
Результаты работы приложения в целом есть в презентации
Результаты генерации есть в файлах: 
* AIfacesGenerator\network\results\my_results 
* AIfacesGenerator\network\results\generated 
* AIfacesGenerator\network\src\result_test 
* AIfacesGenerator\network\src\result_samples 
