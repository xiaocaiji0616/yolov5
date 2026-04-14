import json
import os
 
name2id = {'hero': 0, 'soldier': 1}  # 标签名称（兼容 sodier/soldier）
       
 
def convert(img_size, box):
    dw = 1. / (img_size[0])
    dh = 1. / (img_size[1])
    x = (box[0] + box[2]) / 2.0 - 1
    y = (box[1] + box[3]) / 2.0 - 1
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
 
 
def decode_json(json_floder_path, json_name):
    txt_folder = r'D:\File\python\yolov5\yolov5\packtxt'
    os.makedirs(txt_folder, exist_ok=True)
    txt_name = os.path.join(txt_folder, json_name[0:-5] + '.txt')
    # 存放txt的绝对路径
 
    json_path = os.path.join(json_floder_path, json_name)
    data = None
    for enc in ('utf-8', 'gb2312'):
        try:
            with open(json_path, 'r', encoding=enc, errors='ignore') as jf:
                data = json.load(jf)
            break
        except Exception:
            continue
    if data is None:
        print(f"[WARN] 跳过无法解析的文件: {json_path}")
        return
 
    img_w = data['imageWidth']
    img_h = data['imageHeight']

    with open(txt_name, 'w', encoding='utf-8') as txt_file:
        for i in data['shapes']:

            label_name = i['label']
            if i['shape_type'] == 'rectangle' and label_name in name2id:
                x1 = int(i['points'][0][0])
                y1 = int(i['points'][0][1])
                x2 = int(i['points'][1][0])
                y2 = int(i['points'][1][1])

                bb = (x1, y1, x2, y2)
                bbox = convert((img_w, img_h), bb)
                txt_file.write(str(name2id[label_name]) + " " + " ".join([str(a) for a in bbox]) + '\n')
 
 
if __name__ == "__main__":
 
    json_floder_path = r'D:\File\python\yolov5\wzry\datasets\images\train'
    # 存放json的文件夹的绝对路径
    json_names = [f for f in os.listdir(json_floder_path) if f.lower().endswith('.json')]
    for json_name in json_names:
        decode_json(json_floder_path, json_name)
