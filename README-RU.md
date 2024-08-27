[![Static Badge](https://img.shields.io/badge/Телеграм-Наш_канал-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/hidden_coding)

[![Static Badge](https://img.shields.io/badge/Телеграм-Наш_чат-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/hidden_codding_chat)

[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/catsgang_bot/join?startapp=eVMDZF6Fxdb8eNnjocoOP)

## Рекомендация перед использованием

# 🔥🔥 Используйте PYTHON версии 3.10 🔥🔥

> 🇪🇳 README in english available [here](README)

## Функционал  
|                       Функционал                        | Поддерживается |
|:-------------------------------------------------------:|:--------------:|
|                     Многопоточность                     |       ✅        | 
|                Привязка прокси к сессии                 |       ✅        | 
|                 Авто выполнение квестов                 |       ✅        |
| Авто регистрация аккаунтов по вашей реферальной ссылке  |       ✅        |
| Поддержка tdata / pyrogram .session / telethon .session |       ✅        |


## [Настройки](https://github.com/HiddenCodeDevs/CatsGangBot/blob/main/.env-example/)
|        Настройки        |                                                      Описание                                                       |
|:-----------------------:|:-------------------------------------------------------------------------------------------------------------------:|
|  **API_ID / API_HASH**  |                 Данные платформы, с которой будет запущена сессия Telegram (по умолчанию - android)                 |
|  **DO_CHANNELS_TASKS**  | Выполнять задания, где требуется вход в канал, НЕ РЕКОМЕНДУЮ ВКЛЮЧАТЬ ЕСЛИ АККАУНТЫ НОВОРЕГИ (по умолчанию - False) |
|       **REF_ID**        |                       Ваш реферальный код, идет после '?startapp=' в вашей реферальной ссылке                       |
| **USE_PROXY_FROM_FILE** |                       Использовать ли прокси из файла `bot/config/proxies.txt` (True / False)                       |

## Быстрый старт 📚

Для быстрой установки и последующего запуска - запустите файл run.bat на Windows или run.sh на Линукс

## Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/) **версии 3.10**

## Получение API ключей
1. Перейдите на сайт [my.telegram.org](https://my.telegram.org) и войдите в систему, используя свой номер телефона.
2. Выберите **"API development tools"** и заполните форму для регистрации нового приложения.
3. Запишите `API_ID` и `API_HASH` в файле `.env`, предоставленные после регистрации вашего приложения.

## Установка
Вы можете скачать [**Репозиторий**](https://github.com/HiddenCodeDevs/CatsGangBot) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
git clone https://github.com/HiddenCodeDevs/CatsGangBot.git
cd CatsGangBot
```

Затем для автоматической установки введите:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux ручная установка
```shell
sudo sh install.sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Здесь вы обязательно должны указать ваши API_ID и API_HASH , остальное берется по умолчанию
python3 main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/CatsGangBot >>> python3 main.py --action (1/2)
# Or
~/CatsGangBot >>> python3 main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```


# Windows ручная установка
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Указываете ваши API_ID и API_HASH, остальное берется по умолчанию
python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/CatsGangBot >>> python main.py --action (1/2)
# Или
~/CatsGangBot >>> python main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```




### Контакты

Для поддержки или вопросов, свяжитесь со мной в Telegram:

[![Static Badge](https://img.shields.io/badge/Телеграм-автор_бота-link?style=for-the-badge&logo=telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/pakistankiller)
