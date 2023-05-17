# Результаты тестирования пропускной способности Clickhouse и Vertica
## Запуск тестов
В каталогах clickhouse и vertica выполнить команды:
```shell
docker-compose up -d
python run_tests.py
docker-compose down
```
# Clickhouse
### Тест скорости вставки записей (всего 10 млн)
Вставка осуществляется пачками по 10000 записей, т.е. 50000 записей = 5 пачек, 100000 записей = 10 пачек и т.д.
```
Вставка 50000 записей заняла 0.6911623477935791 сек
Скорость вставки: 72341.90369255022 записей/сек

Вставка 100000 записей заняла 1.289473533630371 сек
Скорость вставки: 77551.02946429694 записей/сек

Вставка 150000 записей заняла 2.042975902557373 сек
Скорость вставки: 73422.30508555278 записей/сек

Вставка 200000 записей заняла 2.6241893768310547 сек
Скорость вставки: 76214.01174998964 записей/сек

Вставка 500000 записей заняла 6.567909002304077 сек
Скорость вставки: 76127.7295140045 записей/сек

Вставка 1000000 записей заняла 13.128153562545776 сек
Скорость вставки: 76172.17419309975 записей/сек

Вставка 3000000 записей заняла 39.59708333015442 сек
Скорость вставки: 75763.15596243438 записей/сек

Вставка 5000000 записей заняла 65.96850085258484 сек
Скорость вставки: 75793.74906780355 записей/сек
```
### Тест скорости чтения записей
Получить все записи с 1 января 2022 года по 1 января 2023 года:
```
Чтение 6252565 записей заняло 17.530140161514282 сек
Скорость чтения: 356675.12880056136 записей/сек
```
# Vertica
### Тест скорости вставки записей (всего 10 млн)
Вставка осуществляется пачками по 10000 записей, т.е. 50000 записей = 5 пачек, 100000 записей = 10 пачек и т.д.
```
Вставка 50000 записей заняла 1.2697834968566895 сек
Скорость вставки: 39376.79149537971 записей/сек

Вставка 100000 записей заняла 2.609485387802124 сек
Скорость вставки: 38321.732119077475 записей/сек

Вставка 150000 записей заняла 3.9496068954467773 сек
Скорость вставки: 37978.46316627723 записей/сек

Вставка 200000 записей заняла 5.279332399368286 сек
Скорость вставки: 37883.577859945246 записей/сек

Вставка 500000 записей заняла 13.01943302154541 сек
Скорость вставки: 38404.13013167065 записей/сек

Вставка 1000000 записей заняла 26.309515476226807 сек
Скорость вставки: 38009.061812772525 записей/сек

Вставка 3000000 записей заняла 79.08940529823303 сек
Скорость вставки: 37931.75569708101 записей/сек

Вставка 5000000 записей заняла 130.0593957901001 сек
Скорость вставки: 38443.97376771907 записей/сек
```
### Тест скорости чтения записей
Получить все записи с 1 января 2022 года по 1 января 2023 года:
```
Чтение 6255388 записей заняло 51.76729202270508 сек.
Скорость чтения: 120836.68578330104 записей/сек.
```
# Итог тестирования
Исходя из результатов, полученных выше, мы можем сделать вывод, что **Clickhouse** значительно 
быстрее обрабатывает запросы как на вставку записей (практически в два раза!), так и на чтение 
записей (практически в 3 раза!). И это еще с учетом того, что мы использовали последнюю на данный 
момент версию Vertica, в отличие от Clickhouse! Следовательно, наш выбор в данном проекте - это **Clickhouse**!