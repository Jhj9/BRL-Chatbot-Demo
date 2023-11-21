# 출렁다리 질의응답 챗봇 프로그램
출렁다리 질의응답 챗봇 프로그램

프로그램 소개
질문을 받으면 주어진 출렁다리 관련 매뉴얼을 참고하여 질문에 대한 답을 포함한 답변을 생성하는 과정을 사용자들이 쉽게 체험해 볼 수 있도록 개발된 챗봇 프로그램이다. 무료 오픈소스 웹 어플리케이션 프레임워크인 Django를 이용해 제작되었으며, 프로그램의 개발을 위해 HTML, CSS, JavaScript, Python 등의 언어가 사용되었다. <br>

주요 기능
- 출렁다리 챗봇 프로그램의 전반적인 설명을 제공한다. <br>
- 사용자가 출렁다리 관련 질문을 입력하면 질문과 관련된 출렁다리 매뉴얼의 문맥을 찾는다. <br>
- 추출된 문맥으로부터 질문에 해당하는 답변을 찾는다. <br>
- 질문, 답변, 문맥을 활용하여 최종 응답을 생성하여 출력한다. <br>

사용 방법
1. 왼쪽 상단의 탭에서 Description 페이지와 Demo 페이지로 이동할 수 있다. <br>
2. Description - 챗봇 프로그램에 대한 정보를 얻을 수 있다. <br>
3. Demo - 실제 챗봇 프로그램을 실행해볼 수 있다. <br>
3-1. 질문을 입력하고 Send 버튼을 누르면 답변이 생성된다. <br>
3-2. 모델이 생성한 답변, 매뉴얼의 문맥 및 해당 문맥이 어떤 매뉴얼에서 추출되었는지에 대한 내용이 출력된다. <br>
3-3. 계속해서 질문을 입력하여 테스트 해볼 수 있다. <br>

Pycharm

![화면 캡처 2022-04-13 141152](https://user-images.githubusercontent.com/50137851/163105666-d975d5a9-6f46-4015-bd12-92cf726cc163.png)

1) Get from VCS로 시작하기

2) https://github.com/Jhj9/BRL-Chatbot-Demo.git clone<br>

3) pip install -r requirements.txt<br>

5) mysite/secrets.json 생성 후 SECRET_KEY 입력 <br>
  Ex) {"SECRET_KEY": "django-insecure-dml=장고시크릿키50자"} <br>
  https://djecrety.ir/

6) python manage.py runserver<br>

7) http://127.0.0.1:8000/ 웹페이지 실행
