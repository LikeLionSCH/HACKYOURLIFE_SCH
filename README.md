# HACKYOURLIFE_SCH
## 🦁 SCH LIKELION HOMEPAGE PROJECT  

## 🚩2020. 11. 19 Project Start

- 🌈 멋쟁이사자처럼 at 순천향대학교 WEB PAGE SERVICE  


## 👨‍👨‍👨‍👧‍👧Creater Member

### 🔙Back-end
- [김율희](https://github.com/yulhee741) 🚩Team Leader
- [이남준](https://github.com/ningpop)
- [황상범](https://github.com/HwangSB)
### 🔜Front-end
- [장하얀](https://github.com/white-jang) 🚩Team Leader
- [최민석](https://github.com/minsgy)
- [하유민](https://github.com/qhahd78)
- [김태완](https://github.com/wwan13)
- [강민서](https://github.com/mseo39)


## 📑 Project Specification

- [HACKYOURLIFE_SCH - Google Docs](https://docs.google.com/document/d/1a0cSXchb96LsK2EMrAxo3-F6dukYH6EYYl73jfSPJ3I/edit)

## ⏱Installation
- Django==3.1.3
- Python3
- Firebase
- Google Calender API
- Google Cloud Platform
- HTML5
- CSS3
- JS
- JQuery


## Commit Rule

- 커밋 메세지 작성시 '[nickname] : message' 의 형식으로 작성 

- 네이밍은 다음과 같이 작성함.

  - Front-end
    - Point
      - 시멘틱 Web 구성 신경 쓰기. (center, main, header, footer)
      - Flex 남발 금지. (적재적소에만 사용하기. 반응형에 알맞는 곳)
      - class name 작성 시, 띄어쓰기 '-'로 사용. `<div class='logo-item'></div>`
    
    - templates
      - VS Code - settings - format on save 켜서 코드 정리 자동화
      - 페이지 최상단에 주석으로 페이지 간략 설명, 작성일 표기
      - 백엔드가 봤을 때 필요한 기능들을 단 번에 알 수 있도록 하기
      - 한 문서에서 동일한 ID 2번 이상 사용하지 않음.
      - CSS 작성시 base.html 의 스타일을 확인한 뒤 중복된 선택자 없이 작성
      
  - Back-end
    - Model Class
      - 모델 클래스의 첫 글자는 대문자로 한다.

    - App Folder
      - APP 폴더 이름은 첫 글자는 소문자로 한다.
      - APP 폴더 이름은 기능이 복수 일 경우, 's'를 붙힌다.
      - 예) comments, users

    - View Function
      - 함수(메소드)에 낙타 표기법 적용
        - 예) getName() ...
      - 변수(필드)에 팟홀 표기법 적용
        - 예) MyFirstVariable -> my_first_variable

    - Templates
      - templates 폴더는 APP 폴더 별로 나누어 관리한다.

    - Static
      - 각 App 폴더 static 폴더를 생성하여 저장한다.
      - `python manage.py collectstatic` 을 통해 모든 static 파일을 모은다.
      - css
        - css를 담는 폴더 명이며, css 명은 html과 동일 시 한다.
      - js
        - js를 담는 폴더 명이며, js 명은 html과 동일 시 한다.
        
    - Documentation
      - [Back-end 데이터베이스 명세서](https://docs.google.com/spreadsheets/d/1w44ECmZIkchegkOk6bUQQR2PjDo5BCTfZ1w3ku5B9KU/edit?usp=sharing)
      - [Back-end 11.23 회의록](https://docs.google.com/document/d/1t1QBOriV5fzJBd1I0WC24otqdxEiOE_ntMQWqOL8iSQ/edit?usp=sharing)
