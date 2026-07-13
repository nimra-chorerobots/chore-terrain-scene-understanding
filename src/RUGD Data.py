import os
import cv2
import numpy as np

# ================= PATHS =================
IMG_DIR = r"D:\Chore\codes\RUGD_frames-with-annotations\RUGD_frames-with-annotations"
ANN_DIR = r"D:\Chore\codes\RUGD_annotations\RUGD_annotations"
COLORMAP_PATH = r"D:\Chore\codes\RUGD_annotations\RUGD_annotations\RUGD_annotation-colormap.txt"

# ================= PARAMETERS =================
ROBOT_WIDTH = 180
SAFETY_MARGIN = 80
BOTTOM_RATIO = 0.75

TRAVERSABLE = {"dirt","sand","grass","asphalt","gravel","mulch","rock-bed","concrete"}

# ================= LOAD COLORMAP (FIXED) =================
def load_rugd_colormap(file_path):
    color_map = {}

    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) < 5:
                continue

            # FORMAT: index label R G B
            label = parts[1]
            r, g, b = int(parts[2]), int(parts[3]), int(parts[4])

            # convert to BGR
            color_map[label] = np.array([b, g, r], dtype=np.uint8)

    return color_map

CLASS_COLORS = load_rugd_colormap(COLORMAP_PATH)

print("Loaded classes:", list(CLASS_COLORS.keys()))

# ================= BUILD LABEL MAP =================
def build_label_map(ann, class_colors):
    h, w = ann.shape[:2]
    label_map = np.full((h, w), -1, dtype=np.int32)

    colors = list(class_colors.values())

    for idx, color in enumerate(colors):
        mask = np.all(ann == color, axis=2)
        label_map[mask] = idx

    # fallback (in case of slight mismatch)
    if np.any(label_map == -1):
        pixels = ann.reshape(-1,3).astype(np.int16)
        table = np.array(colors).astype(np.int16)

        dists = np.sum((pixels[:,None,:] - table[None,:,:])**2, axis=2)
        nearest = np.argmin(dists, axis=1)

        label_map = nearest.reshape(h,w)

    return label_map

# ================= LOAD FILES =================
image_paths = []

for folder in os.listdir(IMG_DIR):
    folder_path = os.path.join(IMG_DIR, folder)
    if not os.path.isdir(folder_path):
        continue

    for file in os.listdir(folder_path):
        if file.endswith(".png"):
            image_paths.append(os.path.join(folder_path, file))

image_paths = sorted(image_paths)

print("Total images:", len(image_paths))

# ================= LOOP =================
index = 0
paused = False

while True:

    if not paused:

        img_path = image_paths[index]
        folder = img_path.split("\\")[-2]
        file_name = os.path.basename(img_path)
        ann_path = os.path.join(ANN_DIR, folder, file_name)

        if not os.path.exists(ann_path):
            index = (index + 1) % len(image_paths)
            continue

        img = cv2.imread(img_path)
        ann = cv2.imread(ann_path)

        if img is None or ann is None:
            index = (index + 1) % len(image_paths)
            continue

        h, w = img.shape[:2]

        # ================= LABEL MAP =================
        label_map = build_label_map(ann, CLASS_COLORS)

        class_names = list(CLASS_COLORS.keys())
        seg_vis = np.zeros_like(img)

        drivable_mask = np.zeros((h,w), dtype=bool)
        class_ratios = {}

        # ================= SEGMENTATION =================
        for idx, cls in enumerate(class_names):

            mask = (label_map == idx)
            ratio = np.sum(mask) / (h*w)
            class_ratios[cls] = ratio

            seg_vis[mask] = CLASS_COLORS[cls]

            if cls in TRAVERSABLE:
                drivable_mask |= mask

        # ================= OVERLAY =================
        overlay = cv2.addWeighted(img, 0.6, seg_vis, 0.4, 0)

        # ================= GAP LOGIC =================
        y1 = int(h * BOTTOM_RATIO)
        bottom = drivable_mask[y1:h, :]

        col_free = np.sum(bottom, axis=0) > 5

        robot_center = w // 2
        required = ROBOT_WIDTH + SAFETY_MARGIN

        # LEFT
        left_gap = 0
        for i in range(robot_center-1, -1, -1):
            if col_free[i]:
                left_gap += 1
            else:
                break

        # RIGHT
        right_gap = 0
        for i in range(robot_center, w):
            if col_free[i]:
                right_gap += 1
            else:
                break

        total_gap = left_gap + right_gap

        if total_gap > required:
            decision = "PASSABLE"
            color_dec = (0,255,0)
        else:
            decision = "BLOCKED"
            color_dec = (0,0,255)

        # ================= DRAW =================
        y2 = h

        # left gap
        cv2.rectangle(overlay, (robot_center-left_gap, y1),
                      (robot_center, y2), (0,255,0), 2)

        # right gap
        cv2.rectangle(overlay, (robot_center, y1),
                      (robot_center+right_gap, y2), (0,255,0), 2)

        # robot
        cv2.rectangle(overlay,
                      (robot_center-required//2, y1),
                      (robot_center+required//2, y2),
                      (255,0,0), 3)

        cv2.putText(overlay, f"L:{left_gap} R:{right_gap}",
                    (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.putText(overlay, decision,
                    (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_dec, 4)

        # ================= DASHBOARD =================
        dash = np.zeros((h,400,3), dtype=np.uint8)

        y = 50
        for cls, val in sorted(class_ratios.items(), key=lambda x: -x[1])[:8]:
            cv2.putText(dash, f"{cls}: {val:.2f}", (20,y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 2)
            y += 30

        cv2.putText(dash, f"GAP: {total_gap}", (20,y+20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        cv2.putText(dash, f"REQ: {required}", (20,y+50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

        cv2.putText(dash, decision, (20,y+90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_dec, 3)

        # ================= DISPLAY =================
        combined = np.hstack((img, seg_vis, overlay, dash))
        combined = cv2.resize(combined, (1800,600))

        cv2.imshow("RUGD FINAL FIXED", combined)

        index = (index + 1) % len(image_paths)

    key = cv2.waitKey(200)

    if key == ord('q'):
        break
    elif key == ord('p'):
        paused = not paused

cv2.destroyAllWindows()
