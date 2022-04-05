
import gridfs

# conn = MongoClient(os.environ['DB_URL'])

DB = "flowers"
DB_COLLECTION_CLASSES = "flower_classes"
DB_COLLECTION = "flower"


def get_img_class(group_num, group_prob, conn, num_img_out=3):
    fs = gridfs.GridFS(conn[DB])
    answer = []
    for i in range(len(group_num)):
        img_list = []
        for img in conn[DB][DB_COLLECTION].find({'group': str(group_num[i])}).limit(num_img_out):
            img_list.append(fs.get(img['imageID']).read())
        name = conn[DB][DB_COLLECTION_CLASSES].find_one({'number': str(group_num[i])})
        answer_dict = {
            'name': name['name'],
            'prob': group_prob[i],
            'images': img_list.copy()
        }
        answer.append(answer_dict)
    return answer

# def load_img_db(path):
#     for group in os.listdir(path):
#         for curr_img in os.listdir(path + group):
#             with open(path + group + '/' + curr_img, 'rb') as f:
#                 data = f.read()
#                 image_id = fs.put(data)
#                 meta = {
#                     'imageID': image_id,
#                     'group': group
#                 }
#                 conn[DB][DB_COLLECTION].insert_one(meta)
#
#
# def load_name_db(classes):
#     for class_ in classes:
#         temp_dict = {
#             'number': class_,
#             'name': classes[class_]
#         }
#         conn[DB][DB_COLLECTION_CLASSES].insert_one(temp_dict)
