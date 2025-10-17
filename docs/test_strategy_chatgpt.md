# Стратегия автоматизации тестирования казуальной игры (итоговая)

**Собственный C++‑движок · Android · iOS · Windows · Python + pytest · Jenkins + GitLab · Zephyr**  
Версия: **1.0 (итоговая)** · Дата: **17 октября 2025**

> Назначение: дать команде единый, практичный и детерминированный подход к авто‑регрессии кор‑лупа, монетизации,
> аналитике и LiveOps на Android/iOS/Windows при минимальном флейке и прозрачной трассируемости в Zephyr и CI.

---

## Содержание
- [1. Обзор и цели](#1-обзор-и-цели)
- [2. Область действия и приоритеты](#2-область-действия-и-приоритеты)
- [3. Архитектура и пирамида тестов](#3-архитектура-и-пирамида-тестов)
- [4. Инструментарий и стек](#4-инструментарий-и-стек)
- [5. Интеграция с Zephyr](#5-интеграция-с-zephyr)
- [6. CI/CD: Jenkins + GitLab](#6-cicd-jenkins--gitlab)
- [7. Окружения и конфигурация](#7-окружения-и-конфигурация)
- [8. Управляемость состояния и тестовые данные](#8-управляемость-состояния-и-тестовые-данные)
- [9. Нефункциональные проверки и производительность](#9-нефункциональные-проверки-и-производительность)
- [10. Репортинг и наблюдаемость](#10-репортинг-и-наблюдаемость)
- [11. Борьба с флейками](#11-борьба-с-флейками)
- [12. Роли и ответственность](#12-роли-и-ответственность)
- [13. Матрица платформ и устройств](#13-матрица-платформ-и-устройств)
- [14. Структура репозитория автотестов](#14-структура-репозитория-автотестов)
- [15. Примеры автоматизируемых сценариев](#15-примеры-автоматизируемых-сценариев)
- [16. Критерии качества (Quality Gates)](#16-критерии-качества-quality-gates)
- [17. Риски и меры](#17-риски-и-меры)
- [18. План внедрения 30/60/90](#18-план-внедрения-306090)
- [19. Что подготовить сегодня](#19-что-подготовить-сегодня)
- [Приложения](#приложения)

---

## 1. Обзор и цели

**Цели**
- Сократить время регрессии и Time‑to‑Green после каждого MR/сборки.
- Раннее выявление дефектов в кор‑лупе (уровень → бой → награда → мета).
- Надёжная валидация монетизации (IAP, вознаграждаемая реклама) и аналитики.
- Контроль производительности/стабильности на реальных устройствах/ПК.

**Принципы**
- **Риск‑ориентированность**: автоматизируем то, что бьёт по доходу/ретенции.
- **Пирамида тестов**: максимум быстрых **engine‑level** тестов; минимум хрупких UI‑E2E.
- **Детерминизм**: фиксируем RNG **seed** и **время**, стабилизируем сеть.
- **Наблюдаемость**: логи, видео, метрики FPS/время кадра, трассировка аналитики.

---

## 2. Область действия и приоритеты

### 2.1 Поддерживаемые платформы
- **Android**: 2–3 последних мажорных версий; устройства трёх тиров (флагман/средний/бюджет), частоты 60/90/120 Гц.
- **iOS**: текущая + предыдущая мажорная; iPhone (2 поколения) + iPad.
- **Windows**: Windows 10/11; стенды на **NVIDIA / AMD / Intel iGPU**.

### 2.2 Приоритеты
**P1 (каждый PR/каждая сборка)**
- Смок: холодный старт → меню → бой (seeded) → награда; базовые мета‑экраны.
- IAP (песочницы): покупка хард‑валюты, чекаут/квитанция.
- Rewarded video: показ → гарантированная награда.
- Аналитика: `level_start/complete/fail`, `iap_purchase`, `ad_reward` (happy‑path).
- Windows: оконный/полноэкранный режим, смена разрешения, alt‑tab.
  
**P2 (ночные)**
- Расширенная регрессия меты/инвентаря/бустеров/LiveOps.
- Локализация UI (обрезы/влазимость) RU/EN + иероглифическая локаль.
- Производительность: p50/p95 времени кадра, FPS, память.
- Долгие сессии (soak) 2–4 ч, стабильность/утечки.

---

## 3. Архитектура и пирамида тестов

### 3.1 Engine‑level через Automation Bridge (C++)
**Идея**: основной объём тестов идёт через встроенный **Automation Bridge** (RPC/IPC), минуя хрупкий UI‑слой ОС.
- **Транспорт**: gRPC/WebSocket; на Windows — Named Pipe, на мобилках — Unix Domain Socket (dev‑сборки).
- **Команды (примеры)**:  
  `start_level(id, seed)`, `skip_tutorial`, `grant_currency`, `grant_booster`,  
  `force_event(id)`, `set_time(mode=freeze/ff, delta_ms)`, `network(mode)`,  
  `wait_event(name, timeout_ms)`, `get_state(path)`, `get_perf()`.
- **UI test‑ID**: стабильные идентификаторы ключевых узлов UI экспортируются из движка.

Покрываем: генератор поля/матчер, экономика/награды/таймеры, сейв/лоад и конфликты облачного сейва.

### 3.2 OS‑level точечно
- **Android/iOS**: Python‑клиент **Appium** — **только** нативные диалоги (IAP, разрешения), системные флоу. Игровой UI — через Bridge.
- **Windows**: pywin32/WinAPI для оконности, alt‑tab, смены разрешений, захвата окна.

### 3.3 Сквозные E2E‑смоки
- «Старт → бой победа → награда → магазин → IAP → инвентарь».
- «Поражение → оффер → rewarded video → повтор».
- «Облачный сейв → очистка → восстановление».
- «Deeplink в ивент → корректная навигация/гейт».
- Windows‑специфика: пресеты графики, alt‑tab под нагрузкой.

---

## 4. Инструментарий и стек

**Python (ядро)**
- `pytest`, `pytest-xdist` (параллель), `pytest-rerunfailures` (контролируемые ретраи), `allure-pytest` (репорты).
- Комм‑клиенты: `grpcio`/`websockets` (Bridge), `requests` (бэкенд/аналитика).
- Мобильное OS: `Appium-Python-Client` (нативные диалоги/пермишены).
- ADB/логи: `adbutils`/сырой `adb`; iOS — `xcrun`/`idevice*` через обёртки.
- Сеть/моки: **mitmproxy** (подмена/трассировка событий аналитики).
- Windows перф: интеграция с **PresentMon**; системные метрики — `psutil`.

**Перф/стабильность**
- Android: `dumpsys gfxinfo framestats` + счётчики движка.
- iOS: `MetricKit`/инструменты + счётчики движка.
- Windows: PresentMon + счётчики движка.

**Отчёты**
- Allure + JUnit XML; вложения: видео, скриншоты, логи движка/сети/ОС.

---

## 5. Интеграция с Zephyr

**Маркировка тестов**
```python
import pytest

@pytest.mark.zephyr("ZEPHYR-1234")
@pytest.mark.platform("android","ios","windows")
@pytest.mark.priority("P1")
def test_core_loop(...):
    ...
```

**Синхронизация результатов**
- Генерировать JUnit XML/Allure JSON. Пост‑степом CI запускать `tools/zephyr_sync.py`:
```
python tools/zephyr_sync.py --input reports/junit.xml --run "Nightly YYYY‑MM‑DD"
```
- Маппинг: 1 автотест ↔ 1 Test Case; параметризация платформ/уровней — параметрами Test Execution.
- Прикладывать артефакты (видео/скриншоты/логи) к рану.

---

## 6. CI/CD: Jenkins + GitLab

**Поток**
1) GitLab CI собирает билды Android/iOS/Windows → загружает как артефакты.  
2) Триггер Jenkins (Webhook/API) на прогоны на парке устройств/ПК.  
3) Jenkins запускает `pytest` по матрице, публикует Allure/JUnit, синхронизирует Zephyr, возвращает статус в MR.

**Jenkinsfile (фрагмент)**
```groovy
pipeline {
  agent { label 'mobile-windows-farm' }
  options { timestamps() }
  stages {
    stage('Prepare') { steps { sh 'python -m pip install -r qa/requirements.txt' } }
    stage('Deploy Builds') {
      steps {
        sh 'tools/deploy_android.sh build/app.apk'
        sh 'tools/deploy_ios.sh build/app.ipa'
        sh 'powershell -File tools/deploy_windows.ps1 build/Game.exe'
      }
    }
    stage('Pytest Smoke') {
      steps { sh 'pytest -m "smoke and p1" -n auto --alluredir=reports/allure --junitxml=reports/junit.xml' }
    }
    stage('Publish Reports') {
      steps {
        junit 'reports/junit.xml'
        allure includeProperties: false, results: [[path: 'reports/allure']]
      }
    }
    stage('Zephyr Sync') {
      steps { sh 'python tools/zephyr_sync.py --input reports/junit.xml --run "PR Smoke"' }
    }
  }
  post { always { archiveArtifacts artifacts: 'reports/**/*', fingerprint: true } }
}
```

**.gitlab-ci.yml (фрагмент)**
```yaml
stages: [build, e2e]

build:
  stage: build
  script: ./ci/build_all.sh
  artifacts:
    paths: [build/]

trigger-e2e:
  stage: e2e
  script: ./ci/trigger_jenkins.sh build/
  when: on_success
```

---

## 7. Окружения и конфигурация

- **Сборки**: `dev` (Bridge + debug‑меню) → `qa` (как прод, но тест‑ключи) → `rc/release`.
- **Feature flags/Remote config**: фиксированные варианты (A/A), ключ `forceTreatment`.
- **IAP**: Google тест‑аккаунты / Apple Sandbox; **Windows** — мок‑биллинг через Bridge.
- **Реклама**: test mode сеток; валидируем только контракт «reward granted».
- **Аналитика**: debug‑endpoint + `mitmproxy`; JSON‑схемы и контракты.

---

## 8. Управляемость состояния и тестовые данные

- Тест‑аккаунты с предустановленным прогрессом (гостевой/соцсети).
- `TestClock` в движке: freeze/fast‑forward.
- Seed‑реплеи уровней (набор «золотых» сидов по типам поля).
- Фикстуры магазинов/офферов/ивентов (JSON) + схемы.

---

## 9. Нефункциональные проверки и производительность

- **Перф**: p50/p95 времени кадра, FPS, время загрузки, память/аллокации.  
- **Стабильность**: crash‑free в прогоне, ANR/hangs.  
- **Потребление**: CPU/GPU/память трендами; температура/батарея (мобилки).  
- **Сеть**: офлайн/латентность/потери; восстановление подключений.

---

## 10. Репортинг и наблюдаемость

- Allure: шаги, аттачи (видео/скриншоты/логи), `environment.json` (платформа/девайс/билд).
- Дашборды Jenkins: стабильность, длительность, топ‑флейки.
- Перф‑CSV (PresentMon/gfxinfo/движок) как артефакты + тренды.

---

## 11. Борьба с флейками

- Жёсткий детерминизм (seed, время, сеть).
- Ожидания по событиям (`wait_event`) вместо `sleep`.
- Контролируемые ретраи для OS‑слоёв (IAP/пермишены) с лимитом.
- Карантин `@flaky`; SLA на починку ≤ 3 рабочих дня.

---

## 12. Роли и ответственность

- **Engine/Client dev**: Automation Bridge, test‑ID, DI времени/рандома.
- **QA Automation (Python)**: фреймворк, фикстуры, тесты, отчёты, Zephyr‑синк.
- **Build/Release**: пайплайны Jenkins/GitLab, парк устройств/ПК, сертификаты/ключи.
- **LiveOps/Analytics**: схемы событий, стабильные флаги/конфиги.

---

## 13. Матрица платформ и устройств (минимум на старт)

| Платформа | Tier | Примеры |
|---|---|---|
| Android | Флагман | Snapdragon 8‑серии, 120 Гц |
| Android | Средний | Snapdragon 7/6‑серии, 90 Гц |
| Android | Бюджет | Helio/Unisoc, 60 Гц |
| iOS | Телефон | Актуальный + предыдущее поколение |
| iOS | Планшет | Актуальный iPad |
| Windows | GPU | NVIDIA mid, AMD mid, Intel iGPU |

---

## 14. Структура репозитория автотестов

```
/qa
  /framework
    engine_bridge/        # gRPC/WebSocket клиенты и модели
    platform/
      android.py
      ios.py
      windows.py
    perf/
      presentmon.py
      android_gfxinfo.py
    utils/
  /tests
    /smoke
    /regression
  /configs
    android.yaml
    ios.yaml
    windows.yaml
  /tools
    zephyr_sync.py
requirements.txt
pytest.ini
```

`pytest.ini`
```ini
[pytest]
markers =
  zephyr(id): Link to Zephyr test case
  platform(*names): Platforms to run on
  component(name): Component tag
  priority(level): P1/P2 tag
  smoke: Smoke tests
```

---

## 15. Примеры автоматизируемых сценариев

**Список ядра (P1)**
1) Холодный старт → меню (верификация ресурсов/версий).  
2) Туториал: `skip`/прохождение через Bridge; фикс‑seed поля.  
3) Бой‑победа: начисление валюты/звёзд, прогресс.  
4) Поражение → оффер → rewarded → повтор.  
5) Магазин: покупка хард‑валюты (песочница), квитанция.  
6) Инвентарь/бустеры: покупка/применение.  
7) LiveOps‑ивент: `force_event` → deeplink → таймер/шоп.  
8) Облачный сейв: синк → очистка → восстановление.  
9) Офлайн → корректные экраны → восстановление сети.  
10) Windows: fullscreen/windowed, смена разрешения, alt‑tab в бою.

**Пример теста (pytest)**
```python
import pytest

@pytest.mark.zephyr("ZEPHYR-1234")
@pytest.mark.platform("android","ios","windows")
@pytest.mark.component("battle")
@pytest.mark.priority("P1")
@pytest.mark.smoke
def test_core_loop_happy_path(bridge):
    bridge.skip_tutorial()
    bridge.start_level(id=101, seed=20240901)
    bridge.wait_event("level_completed")
    reward = bridge.get_state("last_reward")
    assert reward["coins"] >= 50
```

---

## 16. Критерии качества (Quality Gates)

- **PR‑смок** ≤ **10 мин**, 100% зелёных кор‑сценариев, 0 критических падений.  
- **Ночные**: crash‑free ≥ **99.5%**, p95 кадра ≤ **33 мс** (целевой mid‑Android / средний ПК / актуальный iPhone).  
- **Аналитика**: 0 ошибок схем на ключевых событиях; payload соответствует контрактам.

---

## 17. Риски и меры

| Риск | Мера |
|---|---|
| Нет тест‑хуков в движке | Приоритетное внедрение **Automation Bridge** и test‑ID |
| Хрупкие нативные диалоги | Изоляция в отдельные тесты, Appium‑слой + ретраи с лимитом |
| Разнородность Windows (драйверы/GPU) | Фикс версии драйверов на стендах, baseline пресеты |
| Флейки из‑за времени/сети | `TestClock`, стабилизация сети (tc/роутер), моки бэкенда/аналитики |

---

## 18. План внедрения 30/60/90

**0–30 дней**  
- Спецификация API **Automation Bridge** и минимальная реализация.  
- Базовый фреймворк pytest + Allure, фикстуры платформ.  
- PR‑смок: старт → бой → награда (seeded), магазин, IAP (песочница), rewarded.  
- Jenkins job + связка с GitLab; JUnit/Allure артефакты.

**31–60 дней**  
- Ночные регрессии + перф‑съём (движок/PresentMon/gfxinfo).  
- Контракты аналитики + `mitmproxy` трассировка.  
- Windows‑сценарии (режимы экрана, пресеты).  
- Интеграция с **Zephyr** (маппинг кейсов, авто‑синк).

**61–90 дней**  
- Расширение LiveOps/Deeplink/облачный сейв.  
- Локализация/негатив по сети/soak‑прогоны.  
- Расширение матрицы устройств; шардинг/кэш билда для ускорения.

---

## 19. Что подготовить сегодня

- ТЗ на **Automation Bridge** (команды/события/каналы IPC).  
- Таблица **test‑ID** для ключевых экранов/элементов.  
- Базовые конфиги `configs/*.yaml` для Android/iOS/Windows.  
- Jenkins job + Allure плагин; триггер из GitLab.  
- `tools/zephyr_sync.py` и правила маппинга кейсов/ранов.

---

## Приложения

### A. Черновик контракта Automation Bridge (JSON over WebSocket)
```json
// -> Request
{ "cmd": "start_level", "args": { "id": 101, "seed": 20240901 } }
// <- Event
{ "event": "level_completed", "payload": { "stars": 3, "coins": 75 } }
// -> Query
{ "cmd": "get_state", "args": { "path": "last_reward" } }
```

### B. Конвенции test‑ID
- `qa_id` уникален в пределах экрана, стабильный между сборками.
- Нельзя кодировать локализованный текст в `qa_id`.
- Версионировать изменения `qa_id` через changelog для QA.

### C. Пример pytest.ini и маркеров — см. разделы 14 и 15.

### D. Минимальный API для перф
- `get_perf()` возвращает p50/p95 времени кадра, средний FPS, память, длительность загрузок.

---

_Владельцы документа_: QA Automation Lead · Client/Engine Lead · Release/Build Owner  
_Частота пересмотра_: раз в спринт / при значимых изменениях архитектуры
