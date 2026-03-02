# 2WIN (Digital Twin Consciousness Engine - DTCE)

[Türkçe sürüm için aşağıya kaydırın / Scroll down for the Turkish version](#türkçe)

## Overview
**2WIN** (formerly known as DTCE - Digital Twin Consciousness Engine) is a professional, production-grade system designed to create, manage, and simulate digital twin consciousness models. The project focuses on high modularity, scalability, and performance with a robust architecture for cognitive modeling and prediction.

## Key Features
- **Advanced Prediction Engine:** Multi-model support for highly accurate forecasting based on various inputs.
- **Enhanced Cognitive Map:** Temporal tracking and multi-layer capabilities for complex cognitive structuring.
- **Identity & Anomaly Recognition:** Sophisticated fingerprinting and identity recognition systems tailored for robust anomaly detection.
- **Simulation Environment:** Multi-timeline "what-if" scenario generation and testing.
- **High Performance:** Designed with strict adherence to low CPU overhead and asynchronous operations.
- **Reliability:** Built-in robust error handling and comprehensive unit testing frameworks.

## Architecture
The system is cleanly divided into multiple core modules:
- `dtce/prediction/`: Contains the predictive modeling algorithms.
- `dtce/core/`: Interfaces and the fundamental heartbeat of the engine.
- `dtce/simulation/`: Handles the presence and simulation execution.
- `dtce/identity/`: Manages unique entity fingerprinting and identity.
- `dtce/collectors/`: Gathers necessary input timings and external telemetry.

## How It Works (Çalışma Mantığı)
At its core, 2WIN operates iteratively through the following lifecycle:

1. **Input Collection & Recognition (`twin/collectors/`, `twin/identity/`)**
   - Receives events, keystrokes, and telemetry from users.
   - Extracts unique entity "fingerprints" to distinguish individual models dynamically.
2. **Cognitive Processing (`twin/core/`)**
   - The engine updates the internal "cognitive map" using the multi-layered neural graph representation.
   - It tracks state changes over time (temporal tracking).
3. **Prediction & Simulation (`twin/prediction/`, `twin/simulation/`)**
   - Predictive algorithms (e.g., Markov Models or advanced ML) estimate future states or anomalies.
   - Simulators run "what-if" timelines in the background to validate these predictions without affecting the main loop.
4. **Action & Storage**
   - Results are fed back into the cognitive map.
   - Using asynchronous repositories (`twin/storage/`), data is safely logged to non-blocking SQlite engines (`twin_history_v2.db`).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/EmirhanEtem/2WIN.git
   cd 2WIN
   ```
2. Set up a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
*Instructions for running the simulation and interfacing with the engine will be continually updated in the documentation.*

---

# Türkçe

## Genel Bakış
**2WIN** (eski adıyla DTCE - Dijital İkiz Bilinç Motoru), dijital ikiz bilinç modelleri oluşturmak, yönetmek ve simüle etmek için tasarlanmış profesyonel, üretim düzeyinde bir sistemdir. Proje, bilişsel modelleme ve tahmin için sağlam bir mimari ile yüksek modülerlik, ölçeklenebilirlik ve performansa odaklanmaktadır.

## Temel Özellikler
- **Gelişmiş Tahmin Motoru:** Çeşitli girdilere dayalı yüksek doğruluklu tahminler için çoklu model desteği.
- **Gelişmiş Bilişsel Harita:** Karmaşık bilişsel yapılandırma için zamansal izleme ve çok katmanlı yetenekler.
- **Kimlik ve Anormallik Tanıma:** Sağlam anormallik tespiti için özel olarak tasarlanmış gelişmiş parmak izi ve kimlik tanıma sistemleri.
- **Simülasyon Ortamı:** Çoklu zaman çizelgesine sahip "ne olursa" (what-if) senaryosu oluşturma ve test etme.
- **Yüksek Performans:** Düşük CPU kullanımı ve asenkron operasyonlara sıkı sıkıya bağlı kalınarak tasarlanmıştır.
- **Güvenilirlik:** Yerleşik sağlam hata yönetimi ve kapsamlı birim testi çerçeveleri.

## Mimari
Sistem, birden fazla çekirdek modüle temiz bir şekilde ayrılmıştır:
- `dtce/prediction/`: Tahmine dayalı modelleme algoritmalarını içerir.
- `dtce/core/`: Arayüzleri ve motorun temel yapı taşlarını barındırır.
- `dtce/simulation/`: Varlık (presence) ve simülasyon yürütme işlemlerini yönetir.
- `dtce/identity/`: Benzersiz varlık parmak izi çıkarma ve kimlik yönetimini üstlenir.
- `dtce/collectors/`: Gerekli girdi zamanlamalarını ve telemetriyi toplar.

## Çalışma Mantığı (How It Works)
2WIN özünde aşağıdaki yaşam döngüsü üzerinden yinelemeli olarak çalışır:

1. **Girdi Toplama ve Tanıma (`twin/collectors/`, `twin/identity/`)**
   - Kullanıcılardan olayları, tuş vuruşlarını ve telemetriyi alır.
   - Bireysel modelleri dinamik olarak ayırt etmek için benzersiz "parmak izleri" çıkarır.
2. **Bilişsel İşleme (`twin/core/`)**
   - Motor, çok katmanlı sinirsel grafik gösterimini kullanarak dahili "bilişsel haritayı" günceller.
   - Zaman içindeki durum değişikliklerini (zamansal izleme) takip eder.
3. **Tahmin ve Simülasyon (`twin/prediction/`, `twin/simulation/`)**
   - Tahmine dayalı algoritmalar (örn. Markov Modelleri) gelecekteki durumları veya anormallikleri tahmin eder.
   - Simülatörler, ana döngüyü etkilemeden bu tahminleri doğrulamak için arka planda "ne olursa" (what-if) zaman çizelgeleri çalıştırır.
4. **Eylem ve Depolama**
   - Sonuçlar tekrar bilişsel haritaya beslenir.
   - Asenkron veri havuzları (`twin/storage/`) kullanılarak veriler, engellemeyen SQlite motorlarına (`twin_history_v2.db`) güvenle kaydedilir.

## Kurulum
1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/EmirhanEtem/2WIN.git
   cd 2WIN
   ```
2. Sanal bir ortam oluşturun (önerilir):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows üzerinde `venv\Scripts\activate` kullanın
   ```
3. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Kullanım
*Simülasyonu çalıştırma ve motorla etkileşime girme talimatları belgelerde sürekli olarak güncellenecektir.*
