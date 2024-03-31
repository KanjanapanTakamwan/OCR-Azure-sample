from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

subscription_key = "7b7d351c702e4332a6aac818d3222f54"
endpoint = "https://demo-orc-python.cognitiveservices.azure.com/"

credentials = CognitiveServicesCredentials(subscription_key)
client = ComputerVisionClient(endpoint, credentials)

def correct_text_ocr(image_path):
    data = []
    with open(image_path, "rb") as image:
        result = client.recognize_printed_text_in_stream(image)
        for region in result.regions:
            for line in region.lines:
                for word in line.words:
                    bounding_box = word.bounding_box.split(',')
                    x, y, w, h = map(int, bounding_box)
                    bounding_box_str = {"x": x, "y": y, "w": w, "h": h}
                    data.append({"text": word.text, "position": bounding_box_str})
    return data

def filter_data_by_text_and_coordinates(data, text=None, x=None, y=None, h=None, w=None):
    filtered_data = []
    for item in data:
        if (text is None or item['text'] == text) and \
           (x is None or item['position']['x'] == x) and \
           (y is None or item['position']['y'] == y) and \
           (h is None or item['position']['h'] == h) and \
           (w is None or item['position']['w'] == w):
            filtered_data.append(item)
    return filtered_data


def filter_data_by_text_and_coordinates_by_length(data, text=None, x_min=None, x_max=None, y_min=None, y_max=None, h_min=None, h_max=None, w_min=None, w_max=None):
    filtered_data = []
    for item in data:
        x = item['position']['x']
        y = item['position']['y']
        h = item['position']['h']
        w = item['position']['w']
        
        if (text is None or item['text'] == text) and \
           (x_min is None or x >= x_min) and \
           (x_max is None or x <= x_max) and \
           (y_min is None or y >= y_min) and \
           (y_max is None or y <= y_max) and \
           (h_min is None or h >= h_min) and \
           (h_max is None or h <= h_max) and \
           (w_min is None or w >= w_min) and \
           (w_max is None or w <= w_max):
            filtered_data.append(item)
    return filtered_data

def findHeader(data):
    filtered_data_x = filter_data_by_text_and_coordinates(data, text='#')
    filtered_shape = filter_data_by_text_and_coordinates(data, text='#')[0] 
    y_min = filtered_shape['position']['y'] - 3
    y_max = filtered_shape['position']['y'] + filtered_shape['position']['h'] + 3
    filtered = filter_data_by_text_and_coordinates_by_length(data, y_min=y_min, y_max=y_max) 
    return filtered

def findCol(data, allData):
    filtered_data_x = filter_data_by_text_and_coordinates(allData, text='#')
    filtered_shape = filter_data_by_text_and_coordinates(allData, text='#')[0] 
    y_min = filtered_shape['position']['y'] +2
    x_min = data['position']['x']-5
    x_max = data['position']['x'] + data['position']['w'] +5
    filtered = filter_data_by_text_and_coordinates_by_length(allData, x_min=x_min, x_max=x_max,y_min=y_min) 
    return filtered

def findRow_F(data, allData): 
    y_min = data['position']['y'] - 2
    y_max = data['position']['y'] + data['position']['h'] + 2
    x_min = data['position']['x'] - 2
    x_max = data['position']['x'] + data['position']['h'] + 82
    filtered = filter_data_by_text_and_coordinates_by_length(allData, y_min=y_min, y_max=y_max, x_min=x_min, x_max=x_max) 
    sorted_filtered = sorted(filtered, key=lambda x: x['position']['x'])  # Sort by x-coordinate
    return sorted_filtered

def findRow_B(data,allData): 
    y_min = data['position']['y'] - 2
    y_max = data['position']['y'] + data['position']['h'] + 2
    x_min = data['position']['x'] + 200
    x_max = data['position']['x'] + 135 + data['position']['h'] + 150
    filtered = filter_data_by_text_and_coordinates_by_length(allData, y_min=y_min, y_max=y_max, x_min=x_min, x_max=x_max) 
    sorted_filtered = sorted(filtered, key=lambda x: x['position']['x'])  # Sort by x-coordinate
    return sorted_filtered

def calculate_imps(player_1_score, player_2_score):
    point_difference = player_1_score - player_2_score
    
    point_difference = abs(point_difference)
    
    imp_table = {
        0: 0, 20: 1, 50: 2, 90: 3, 130: 4, 170: 5, 220: 6, 270: 7, 320: 8,
        370: 9, 430: 10, 500: 11, 600: 12, 750: 13, 900: 14, 1100: 15,
        1300: 16, 1500: 17, 1750: 18, 2000: 19, 2250: 20, 2500: 21, 3000: 22,
        3500: 23, 4000: 24
    }
    
    nearest_key = max(key for key in imp_table.keys() if key <= point_difference)
    if player_1_score < player_2_score :
        return -imp_table[nearest_key]
    else :
        return imp_table[nearest_key]
def contract(data):
    level = data[0:1]
    suit = data[1:2]
    by = data[2:3]
    result = data[3:]
    return level,suit,by,result


image = [1,2,3]

for index, i in enumerate(image):
    print()
    print(f'{index}')
    image_path = "./image/match_{}.jpg".format(i)
    data_json = correct_text_ocr(image_path)
    col_1 = findHeader(data_json)
    
    filtered_col_data = findCol(col_1[0], data_json)
    match = []
    try:
        p_1 = col_1[1]['text']
        p_2 = col_1[-1]['text']
    except Exception as e:
        print(f'player : {e}')
    for index, item in enumerate(filtered_col_data):
        rol_1_F = findRow_F(item, data_json)
        rol_1_B = findRow_B(item, data_json)

        IMPs = None
        try :
            board_id = rol_1_F[0]['text'] if rol_1_F and rol_1_F[0] else None
            p1 = rol_1_F[1]['text'] if rol_1_F and rol_1_F[1] else None
            p1_score = rol_1_F[2]['text'] if rol_1_F and rol_1_F[2] else None
            p2 = rol_1_B[0]['text'] if rol_1_B and rol_1_B[0] else None
            p2_score = rol_1_B[1]['text'] if rol_1_B and rol_1_B[1] else None
        except Exception as e:
            print(f'{e}')  
        try :
            IMPs = calculate_imps(int(rol_1_F[2]['text']), int(rol_1_B[1]['text']))
            level1, suit1, by1, result1 = contract(p1)
            level2, suit2, by2, result2 = contract(p2)
            match.append({"id": board_id, "level1": level1,"suit1": suit1,"by1": by1,"result1": result1,"p1_score":p1_score, "level2": level2,"suit2": suit2,"by2": by2,"result2": result2,"p2_score":p2_score,"IMPs":IMPs})
            for item in enumerate(match):
                print(f"{item}")
        except Exception as e:
            print(f'{e}')          
