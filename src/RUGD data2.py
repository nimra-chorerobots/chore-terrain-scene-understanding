import os
import cv2
import numpy as np

# ================= PATHS =================
IMG_DIR = r"D:\Chore\codes\RUGD_frames-with-annotations\RUGD_frames-with-annotations"
ANN_DIR = r"D:\Chore\codes\RUGD_annotations\RUGD_annotations"

# ================= COLORMAP (FROM YOUR FILE) =================
COLORMAP = {
    "dirt": (108,64,20),
    "sand": (255,229,204),
    "grass": (0,102,0),
    "tree": (0,255,0),
    "pole": (0,153,153),
    "water": (0,128,255),
    "asphalt": (64,64,64),
    "gravel": (255,128,0),
    "building": (255,0,0),
    "mulch": (153,76,0),
    "rock": (153,204,255),
    "bush": (255,153,204),
}

# ================= GROUPING =================
DRIVABLE = ["dirt", "sand", "grass", "asphalt", "gravel"]
OBSTACLE = ["tree", "rock", "bush", "building"]
HAZARD = ["water"]

# ================= MASK =================
def mask(img_rgb, color):
    return np.all(img_rgb == color, axis=2)

# ================= LOAD FILES =================
image_paths = []
for folder in os.listdir(IMG_DIR):
    fpath = os.path.join(IMG_DIR, folder)
    if not os.path.isdir(fpath): continue
    for file in os.listdir(fpath):
        if file.endswith(".png"):
            image_paths.append(os.path.join(fpath, file))

image_paths = sorted(image_paths)

# ================= LOOP =================
i = 0
paused = False

while True:

    if not paused:

        img_path = image_paths[i]
        folder = img_path.split("\\")[-2]
        fname = os.path.basename(img_path)
        ann_path = os.path.join(ANN_DIR, folder, fname)

        if not os.path.exists(ann_path):
            i = (i+1)%len(image_paths)
            continue

        img = cv2.imread(img_path)
        ann = cv2.imread(ann_path)

        if img is None or ann is None:
            i = (i+1)%len(image_paths)
            continue

        # 🔥 convert to RGB
        ann = cv2.cvtColor(ann, cv2.COLOR_BGR2RGB)

        h,w = img.shape[:2]
        seg = np.zeros_like(img)

        drivable_mask = np.zeros((h,w),bool)
        hazard_mask = np.zeros((h,w),bool)

        # ================= CLASS DETECTION =================
        for cls, color in COLORMAP.items():

            m = mask(ann, color)

            if cls in DRIVABLE:
                seg[m] = (0,255,0)
                drivable_mask |= m

            elif cls in OBSTACLE:
                seg[m] = (0,0,255)

            elif cls in HAZARD:
                seg[m] = (255,0,0)
                hazard_mask |= m

        # ================= RATIOS =================
        total = h*w
        drivable_ratio = np.sum(drivable_mask)/total
        hazard_ratio = np.sum(hazard_mask)/total

        # ================= SCENE =================
        if hazard_ratio > 0.05:
            scene = "HAZARD (WATER)"
            speed = 0.1
            color = (255,0,0)

        elif drivable_ratio > 0.5:
            scene = "DRIVABLE"
            speed = 0.8
            color = (0,255,0)

        elif drivable_ratio > 0.25:
            scene = "SEMI-DRIVABLE"
            speed = 0.5
            color = (0,165,255)

        else:
            scene = "NON-DRIVABLE"
            speed = 0.2
            color = (0,0,255)

        # ================= OVERLAY =================
        overlay = cv2.addWeighted(img,0.8,seg,0.3,0)

        cv2.putText(overlay, scene, (50,h//2),
                    cv2.FONT_HERSHEY_SIMPLEX,1.5,color,3)

        # ================= DISPLAY =================
        img_disp = img.copy()
        seg_disp = seg.copy()
        over_disp = overlay.copy()

        cv2.putText(img_disp,"RAW IMAGE",(20,40),0,1,(255,255,255),2)
        cv2.putText(seg_disp,"SEMANTIC SEGMENTATION",(20,40),0,1,(255,255,255),2)
        cv2.putText(over_disp,"SCENE UNDERSTANDING",(20,40),0,1,(255,255,255),2)

        final = np.hstack((img_disp, seg_disp, over_disp))
        final = cv2.resize(final,(1600,600))

        cv2.imshow("FINAL RUGD SYSTEM (CORRECT)", final)

        i = (i+1)%len(image_paths)

    k = cv2.waitKey(200)
    if k == ord('q'): break
    elif k == ord('p'): paused = not paused

cv2.destroyAllWindows()
