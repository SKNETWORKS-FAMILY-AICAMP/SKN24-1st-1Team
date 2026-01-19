# SKN24-1st-1Team

## 도로지킴이 소개

| **김수진** | **김은우** | **박세현** | **조아름** | **정준하** |
|:-:|:-:|:-:|:-:|:-:|
| ⭐️귀요미⭐️ </br> 기획/DB설계/BE  | DB설계/BE | DB설계/FE/화면설계 | DB설계/BE | 화면설계/FE
| [![github - KimSujin02](https://img.shields.io/badge/KimSujin02-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/KimSujin02) | [![github - whitehole17](https://img.shields.io/badge/whitehole17-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/whitehole17) | [![github - parksay](https://img.shields.io/badge/parksay-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/parksay) | [![github - areum117](https://img.shields.io/badge/areum117-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/areum117) | [![github - junhaj27-jpg](https://img.shields.io/badge/junhaj27-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/junhaj27-jpg) |


## 프로젝트 개요
### 👷안전지대👷
> 차량 밀집도 대비 사고 다발 구간 분석을 통한 지자체 맞춤형 인프라 최적화 서비스

단순히 사고가 많이 난 곳이 아니라, 통행량(밀집도) 대비 사고율이 비정상적으로 높은 **'위험 사각지대'** 를 찾아내어 지자체가 제한된 예산 내 가장 효과적인 교통 안전 인프라 설치 지점을 선정할 수 있도록 지원하는 솔루션

## 기술 스택
![python](https://img.shields.io/badge/python-0098FF.svg?style=for-the-badge&logo=python&logoColor=yellow) ![mysql](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white) ![git](https://img.shields.io/badge/git-F05032.svg?style=for-the-badge&logo=git&logoColor=white) ![streamlit](https://img.shields.io/badge/streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white) ![selenium](https://img.shields.io/badge/selenium-43B02A.svg?style=for-the-badge&logo=selenium&logoColor=white) 


## WBS


## 파일 구조
```
.
├── assets/                         # 이미지 파일 저장용 폴더
│
├── crawling/                       # 크롤러 모듈
│   ├── accident.csv                # 교통사고 통계 데이터
│   ├── accident_csv_processor.py   # 교통사고 데이터 csv 프로세서
│   ├── crawler_tbl_veh_cnt.py      # 전국 차량 등록대수 크롤러
│   ├── crawling_city_pop.py        # 인구수 크롤러
│   ├── crawling_faq1.py            # 국토교통부 민원마당 FAQ 크롤러
│   └── crawling_faq2.py            # 한국교통안전공단 FAQ 크롤러
│
├── pages/
│   ├── city_pop_page.py            # 인구 페이지
│   ├── faq_page.py                 # FAQ 페이지
│   └── 
│
├── sql/                            # DB 관련 모듈
│   ├── city_pop_sql.py
│   ├── faq_sql.py
│   └── roadkeeper.sql              # DB 스키마
│
├── streamlit/                      # streamlit 코드 폴더
│   ├── common.py      
│   ├── main.py                     # 메인 페이지
│   └── /pages                      # 페이지 리스트
│       ├── 01_page_accident.py
│       ├── 02_registered_car.py
│       └── 03_faq.py         
│
├── .gitignore                  # Git 제외 파일 설정
├── README.md                   # 프로젝트 개요 및 사용 방법
└── app.py                      
```


요구사항 명세서

ERD

회고

#교통사고 공공 데이터


 1 차종 4가지
 
 승용;
 승합;
 화물;
특수;
