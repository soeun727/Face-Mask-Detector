# import data 하면 이 파일 모두 실행

# 데이터 파트
from urllib.request import Request, urlopen
import json
import os   # 파일정보 감지하기 위함
# 마스크 합성 단계
import face_recognition
from PIL import Image, ImageDraw
import numpy as np

# 다운로드 기능(without_mask, with_mask, mask)
def download_image(kind):
    if kind == 'without_mask':
        api_url = 'https://api.github.com/repos/prajnasb/observations/contents/experiements/data/without_mask?ref=master' # json 형식
        hds = {'User-Agent': 'Mozilla/5.0'}

        request = Request(api_url, headers=hds)  # 요청 보냄
        response = urlopen(request)
        directory_bytes = response.read()
        directory_str = directory_bytes.decode('utf-8')

        contents = json.loads(directory_str)

        for i in range(len(contents)):
            content = contents[i]
            request = Request(content['download_url'])
            response = urlopen(request)
            image_data = response.read()

            if not os.path.exists('data'):
                os.mkdir('data')
            if not os.path.exists('data/without_mask'):
                os.mkdir('data/without_mask')

            image_file = open('data/without_mask/' + content['name'], 'wb') #binary로 write하겠다
            image_file.write(image_data)
            image_file.close()
            print('without_mask 이미지 다운로드 중(' + str(i + 1) + '/' + str(len(contents)) + '): ' + content['name'])
        print('without_mask 이미지 다운로드 완료')

    elif kind == 'with_mask':
        api_url = 'https://api.github.com/repos/prajnasb/observations/contents/experiements/data/with_mask?ref=master'  # json 형식
        hds = {'User-Agent': 'Mozilla/5.0'}

        request = Request(api_url, headers=hds)  # 요청 보냄
        response = urlopen(request)
        directory_bytes = response.read()
        directory_str = directory_bytes.decode('utf-8')

        contents = json.loads(directory_str)

        for i in range(len(contents)):
            content = contents[i]
            request = Request(content['download_url'])
            response = urlopen(request)
            image_data = response.read()

            if not os.path.exists('data'):
                os.mkdir('data')
            if not os.path.exists('data/without_mask'):
                os.mkdir('data/without_mask')

            image_file = open('data/without_mask/' + content['name'], 'wb')  # binary로 write하겠다
            image_file.write(image_data)
            image_file.close()
            print('without_mask 이미지 다운로드 중(' + str(i + 1) + '/' + str(len(contents)) + '): ' + content['name'])
        print('without_mask 이미지 다운로드 완료')
    elif kind == 'mask':
        mask_image_download_url = 'https://github.com/prajnasb/observations/raw/master/mask_classifier/Data_Generator/images/blue-mask.png'

        request = Request(mask_image_download_url)
        response = urlopen(request)#리스폰스 받으면 url open
        image_data = response.read()

        if not os.path.exists('data'):
            os.mkdir('data')

        image_file = open('data/mask.png', 'wb')
        image_file.write(image_data)
        image_file.close()
        print('mask 이미지 다운로드 완료')

# 점과 점사이의 거리
def distance_point_to_point(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# 점과 직선 사이의 거리
def distance_point_to_line(point, line_point1, line_point2):
    if line_point1[0] == line_point2[0]:
        return np.abs(point[0] - line_point1[0])
    a = -(line_point1[1] - line_point2[1]) / (line_point1[0] - line_point2[0])
    b = 1
    c = -a * line_point1[0] - b * line_point1[1]
    return np.abs(a * point[0] + b * point[1]+c) / np.sqrt(a ** 2 + b ** 2)

def rotate_point(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return qx, qy

# 마스크 합성
def mask_processing(face_image_file_name):
    #이미지 불러오기
    face_image_path='data/without_mask/' + face_image_file_name # 이미지에 대한 전체 경로
    mask_image_path = 'data/mask.png'

    # 얼굴 영역 추출, 얼굴 랜드마크 추출
    face_image_np = face_recognition.load_image_file(face_image_path)
    face_locations = face_recognition.face_locations(face_image_np)
    face_landmarks = face_recognition.face_landmarks(face_image_np, face_locations)

    # 결과 이미지 생성
    face_image=Image.fromarray(face_image_np) # 배열 정보로 이미지 생성
    mask_image = Image.open(mask_image_path)

    face_count = 0 # 얼굴이 인식이 되어야 학습이 되는데, 얼굴이 인식이 안되는 데이터는 구별이 필요함

    #마스크 합성(핵심 내용)
    for face_landmark in face_landmarks: # 얼굴의 landmark정보가 하나씩 들어가고 이 정보로 합성
        # 예외처리(nose_bridge와 chin이 랜드마크에 없다면 무시
        if ('nose_bridge' not in face_landmark) or ('chin' not in face_landmark):
            continue
        # 마스크 너비의 보정값
        mask_width_ratio = 1.2 #너비 조금 키움

        # 마스크 높이 계산(nose_bridge 2번째 점, chin 9번째 점의 길이)
        mask_height = int(distance_point_to_point(face_landmark['nose_bridge'][1], face_landmark['chin'][8]))

        # 마스크 좌/우 분할 --> 얼굴이 좌우로 돌아갈때 오른쪽/왼쪽 얼굴의 거리 차이가 생기는데, 이런 것들을 맞춰주기 위함
        mask_left_image = mask_image.crop((0, 0, mask_image.width // 2, mask_image.height))
        mask_right_image = mask_image.crop((mask_image.width // 2, 0, mask_image.width, mask_image.height))

        #mask_left_image.show()
        #mask_right_image. show()

        # 왼쪽 얼굴의 너비 계산
        mask_left_width = int(distance_point_to_line(face_landmark['chin'][0], face_landmark['nose_bridge'][0], face_landmark['chin'][8]) * mask_width_ratio) # 맨앞은 점 후자는 직선

        # 왼쪽 마스크 크기 조절
        mask_left_image = mask_left_image.resize((mask_left_width, mask_height))

        # 오른쪽 얼굴 너비 계산
        mask_right_width = int(distance_point_to_line(face_landmark['chin'][16], face_landmark['nose_bridge'][0], face_landmark['chin'][8]) * mask_width_ratio)
        # 오른쪽 마스크 크기 조절
        print(mask_right_width, mask_height)
        mask_right_image = mask_right_image.resize((mask_right_width, mask_height)) #괄호 두개

        # 좌/우 마스크 연결 -> 얼굴 형태에 맞게 비대칭 형태
        mask_image = Image.new('RGBA', (mask_left_width + mask_right_width, mask_height))
        mask_image.paste(mask_left_image, (0,0), mask_left_image)
        mask_image.paste(mask_right_image,(mask_left_width,0), mask_right_image) # 왼쪽 이미지의 너비만큼 떨어진 위치

        mask_image.show()
        # 얼굴 회전 각도 계산
        # x의 변화량
        dx = face_landmark['chin'][8][0] - face_landmark['nose_bridge'][0][0]
        dy = face_landmark['chin'][8][1] - face_landmark['nose_bridge'][0][1]
        face_radian = np.arctan2(dy, dx)
        face_degree = np.rad2deg(face_radian)

        # 마스크 회전
        mask_degree = (90-face_degree + 360) % 360
        mask_image = mask_image.rotate(mask_degree, expand=True)

        # 마스크 위치 계산
        mask_radian = np.deg2rad(-mask_degree)
        center_x = (face_landmark['nose_bridge'][1][0] + face_landmark['chin'][8][0]) // 2 # 중심점 기준으로 회전해야하니까 중심점 정하기(x 좌표)
        center_y = (face_landmark['nose_bridge'][1][1] + face_landmark['chin'][8][1]) // 2 # 중심점 기준으로 회전해야하니까 중심점 정하기(y 좌표)
        p1 = rotate_point((center_x, center_y), (center_x - mask_left_width, center_y - mask_height // 2), mask_radian)
        p2 = rotate_point((center_x, center_y), (center_x - mask_left_width, center_y + mask_height // 2), mask_radian)
        p3 = rotate_point((center_x, center_y), (center_x + mask_left_width, center_y - mask_height // 2), mask_radian)
        p4 = rotate_point((center_x, center_y), (center_x + mask_left_width, center_y + mask_height // 2), mask_radian)

        box_x = int(min(p1[0], p2[0], p3[0], p4[0]))
        box_y = int(min(p1[1], p2[1], p3[1], p4[1]))


        # 마스크 합성(붙여넣기)
        face_image.paste(mask_image, (box_x, box_y), mask_image)
        face_count+=1

   # 결과 이미지 반환
    return face_image, face_count


# 데이터 생성
def generate_data():
    face_image_base_path = 'data/without_mask/'
    save_path = 'data/with_mask/'

    face_image_file_names = os.listdir(face_image_base_path)
    for i in range(len(face_image_file_names)):
        face_image_file_name = face_image_file_names[i]
        face_image, face_count = mask_processing(face_image_file_name)

        if face_count == 0:
            os.remove(face_image_base_path + face_image_file_name)
            print('얼굴 인식 실패(' + str(i+1) + '/' + str(len(face_image_file_names)) + '): ' + face_image_file_name)
        else:
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            face_image.save(save_path + face_image_file_name)
            print('마스크 합성중('+str(i+1) + '/' + str(len(face_image_file_names))+'): ' + face_image_file_name)
        print('마스크 합성 완료')


if __name__ == '__main__':      # 메인함수의 기능을 할 뿐, 이 코드를 직접 실행할때만 실행되고 다른 함수에서 불러서 실행하면 실행 안됨(import data로 실행하면 X)
    #mask_processing('104.jpg')
    generate_data()