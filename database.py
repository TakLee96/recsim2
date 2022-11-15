import json

def load_sequential_json(json_path):
    print(f"loading ... {json_path}")
    data = []
    with open(json_path, "r") as json_file:
        for line in json_file:
            if line.strip():
                data.append(json.loads(line))
    return data


def load_data():
    photo_root = "/Users/lijiahang/Documents/yelp_photos"
    photo_json = "photos.json"
    photo_data = load_sequential_json(f"{photo_root}/{photo_json}")

    dataset_root  = "/Users/lijiahang/Documents/yelp_dataset"
    business_json = "yelp_academic_dataset_business.json"
    business_data = load_sequential_json(f"{dataset_root}/{business_json}")

    # user_json = "yelp_academic_dataset_user.json"
    # user_data = load_sequential_json(f"{dataset_root}/{user_json}")
    
    # review_json = "yelp_academic_dataset_review.json"
    # review_data = load_sequential_json(f"{dataset_root}/{review_json}")

    return photo_data, business_data #, user_data, review_data

KEYS = [ "name", "stars", "review_count", "categories" ]
def index_data(photo_data, business_data):
    print("indexing ...")
    keys_set = set(KEYS)
    business_index = {}
    for business in business_data:
        b = { k: v for k, v in business.items() if k in keys_set }
        b["photos"] = []
        business_index[business["business_id"]] = b
    print(f"loaded {len(business_index)} business")
    
    for photo in photo_data:
        business_index[photo["business_id"]]["photos"].append(photo["photo_id"])
    
    lean_business_index = {}
    for b, v in business_index.items():
        if len(v["photos"]) > 0:
            lean_business_index[b] = v
    print(f"... {len(lean_business_index)} business have photos")

    return lean_business_index

def load_index():
    p, b = load_data()
    i = index_data(p, b)
    return i
