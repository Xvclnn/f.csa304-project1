# F.CSA304-PROJECT1

Энэхүү төсөл нь шүхэртэй үсрэлтийн хөдөлгөөнийг тоон аргаар загварчилж, унах хурд, өндөр, агаарын эсэргүүцэл болон шүхэр нээгдэх мөчийн нөлөөг шинжлэх зорилготой Python төсөл юм. Төсөлд Euler болон RK4 аргуудыг ашиглан симуляци хийж, онолын тооцоотой харьцуулсан шинжилгээ болон график дүрслэлүүдийг гаргасан. Мөн үндсэн функцуудыг шалгах автомат тестүүд багтсан.

## Боломжууд

- Шүхэртэй үсрэлтийн хөдөлгөөнийг хугацааны дагуу симуляцлах
- Euler болон RK4 тоон аргуудын үр дүнг харьцуулах
- Тогтмол болон өндрөөс хамаарах агаарын нягтын загвар ашиглах
- Шүхэр нээгдэхээс өмнөх болон дараах хөдөлгөөнийг тусад нь шинжлэх
- Онолын terminal velocity-г симуляцын үр дүнтэй харьцуулах
- Аюулгүй газардах хурдыг шалгах, шаардлагатай шүхрийн талбайг тооцоолох
- `matplotlib` ашиглан график, зураг үүсгэх
- `pytest` ашиглан үндсэн функцуудыг тестлэх

## Технологийн стек

- Python 3
- NumPy
- Matplotlib
- Pytest

## requirements

Дараах зүйлс систем дээр суусан байх шаардлагатай:

- Python 3.10 or higher
- `pip`

Optional:

- `venv` эсвэл өөр виртуал орчны хэрэгсэл

## Installation

1. Repository clone хийнэ.

```bash
git clone <repository-url>
cd f.csa304-project1
```

2. Virtual орчин үүсгээд идэвхжүүлнэ.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Dependency суулгана.

```bash
pip install -r requirements.txt
```

4. Энэхүү project-д тусгай environment variable шаардлагагүй.

## Ашиглах заавар

### 1. Шинжилгээний үр дүнг гаргах

```bash
python3 src/analysis.py
```

Энэ команд нь:

- онолын болон симуляцын terminal velocity-г харьцуулна
- буух үеийн хурдыг хэвлэнэ
- аюулгүй газардах боломжийг шалгана

### 2. График байгуулах

```bash
python3 src/visualization.py
```

Энэ нь `output/` хавтсанд үр дүн зургуудыг бий болгоно.

### 3. Тест ажиллуулах

```bash
pytest
```

## Жишээ ашиглалт

Python дотроос үндсэн симуляцыг дуудах жишээ:

```python
from src.simulation import simulate_jump

t, v, h = simulate_jump(
    m=85,
    h0=4000,
    t_shuher_zadrah=60,
    dt=0.1,
    method="rk4",
    constant_density=False,
)

print(t[-1], v[-1], h[-1])
```

## Төслийн бүтэц

```text
f.csa304-project1/
├── src/
│   ├── simulation.py      # Үндсэн физик загвар ба тоон интеграц
│   ├── analysis.py        # Онолын харьцуулалт, аюулгүй байдлын шинжилгээ
│   ├── visualization.py   # График дүрслэл, зураг хадгалалт
│   └── tempCodeRunnerFile.py
├── tests/
│   ├── test_simulation.py
│   └── test_analysis.py
├── output/                # Үүсгэсэн зурагууд
├── docs/
│   └── report.odt
├── requirements.txt
└── README.md
```
