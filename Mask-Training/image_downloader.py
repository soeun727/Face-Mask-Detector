#학습할 데이터를 수집하는 단계의 코드

from urllib.request import Request, urlopen # urlopen: 웹 url 연결을 시도해주는, 연결정보를 만들어주는 패키지
#request: html 요청의 응답을 받아오도록
import json
import os

# 0424 새로 추가한 코드(마스크 이미지 다운로드)
def image_download(url, filepath):
    #요청을 보내서 데이터를 받아오기
    request = Request(url)
    response = urlopen(request)
    image_data = response.read()
    file = open(filepath, 'wb') # 바이너리로 쓰기
    file.write(image_data)
    file.close()
    print(url + '로부터' + filepath + '에 다운로드 완료')

# 마스크 다운로드 url
mask_url = 'https://github.com/prajnasb/observations/raw/master/mask_classifier/Data_Generator/images/blue-mask.png'
image_download(mask_url, 'data/mask.png')
exit() # 아래꺼 수행되지 않도록

#-----------------------------------------------------------------------------------------------------------------------

save_folder = 'data/without_mask/' #여기에 전부 저장한다.
#url-어디로 요청을 보낼건지
api_url = 'https://api.github.com/repos/prajnasb/observations/contents/experiements/data/without_mask?ref=master'

headers = {'User-Agent': 'Mozilla/5.0'}  #내가 쓰는 웹엔진은 모질라이다
request = Request(api_url, headers=headers) #요청 보냄
response = urlopen(request)
directory_bytes = response.read()
directory_str=directory_bytes.decode('utf-8')#byte->str로 바꿔줌(디코드)-사람이 읽을 수있는 형태로 1차 가공
contents = json.loads(directory_str) # 통으로 인식할 수 있는 형태, byte문자열 - 가공이 안되어있는 //json: 자바스크립트에서 파일을 계층구조로 표현하기 위한 구조

for i in range(len(contents)):      #i가 contents의 길이만큼 뽑아와서 도는 것
    content = contents[i]       # content가 요소 하나하나가 되는 것
    request = Request(content['download_url'],headers=headers)# download url 을 가져옴 다운하기 위해
    response = urlopen(request) #response로 받아온게 이미지 데이터(가공이 안된 상태)
    data=response.read()    #데이터 읽어서 data에 저장

    #경로 지정
    if not os.path.exists('data'):  #만약 data 폴더가 없다면,
        os.mkdir('data')    #data 폴더를 만들어라
    if not os.path.exists('data/without_mask'):
        os.mkdir('data/without_mask')

    #쓰기 모드로 저장
    file=open(save_folder + content['name'], 'wb') #바이너리 모드로 쓰겠다
    file.write(data)
    print('다운로드 완료(' + str(i+1) +'/' + str(len(contents)) + '): ' + content['name'])
    #다운로드 완료(30/500): 30.jpeg
    break   #하나만 받음



#response = open('data.json')
#directory_str = response.read()  #json으로 변환
#print(directory_str[0])
#response.close()

#response = open('data.json')
#directory_json = json.load(response)  #json으로 변환
#print(directory_json[0]['download_url'])
#response.close()


#directory = response.read()
#print(directory)

#다운로드 자동화하는 코드
