# Chore Terrain Scene Understanding

### Semantic Terrain Classification and Scene Understanding using the RUGD Dataset for Autonomous Outdoor Robotics

This repository implements a semantic terrain understanding pipeline for autonomous robots using the **RUGD (Rensselaer Unstructured Ground Driving) Dataset**. The system analyzes outdoor environments through semantic segmentation, classifies terrain into navigable and hazardous regions, and generates scene-level understanding to support autonomous navigation.

The project demonstrates how semantic segmentation can be transformed into actionable terrain perception by identifying drivable surfaces, obstacles, and hazardous regions suitable for outdoor robotic applications.

---

# 📌 Overview

Autonomous robots operating in parks, gardens, trails, construction sites, and other unstructured environments must understand terrain semantics to navigate safely and efficiently.

This repository presents a lightweight perception pipeline that processes semantic annotations from the RUGD dataset to classify terrain into meaningful navigation categories.

The pipeline performs:

- Semantic segmentation decoding
- Terrain classification
- Scene understanding
- Hazard detection
- Terrain distribution analysis
- Navigation recommendation
- Visualization for perception debugging

The repository is intended for:

- Autonomous robotics
- Terrain perception
- Outdoor navigation
- Semantic segmentation research
- Mobile robotics
- Computer vision education
- Digital twin perception
- Autonomous lawn robots

---

# 🚀 Features

- Semantic segmentation visualization
- Terrain classification
- Drivable region identification
- Semi-drivable terrain analysis
- Obstacle detection
- Water and hazard detection
- Terrain distribution statistics
- Adaptive navigation recommendations
- Visual perception debugging

---

# 📂 Dataset

This project uses the **RUGD (Rensselaer Unstructured Ground Driving) Dataset**, a benchmark dataset for semantic understanding in outdoor environments.

The dataset contains:

- RGB images
- Pixel-wise semantic annotations
- 24 terrain and object classes
- Outdoor scenes including:
  - Grass
  - Dirt
  - Gravel
  - Asphalt
  - Bushes
  - Trees
  - Rocks
  - Water
  - Structures

Example dataset structure:

```text
RUGD/
├── rgb/
├── labels/
├── colormap/
└── annotations/
```

---

# 🔄 Processing Pipeline

```text
RGB Image
      │
      ▼
Semantic Annotation
      │
      ▼
Color Map Decoding
      │
      ▼
Terrain Classification
      │
      ▼
Scene Understanding
      │
      ▼
Terrain Distribution Analysis
      │
      ▼
Hazard Detection
      │
      ▼
Navigation Recommendation
```

---

# ⚙️ Core Components

## 1️⃣ Semantic Segmentation

The pipeline reads pixel-wise semantic annotations from the RUGD dataset and decodes them into meaningful terrain classes.

Outputs include:

- Terrain masks
- Semantic labels
- Scene visualization

---

## 2️⃣ Terrain Classification

Terrain classes are grouped into higher-level navigation categories.

### Drivable

- Grass
- Dirt
- Gravel
- Asphalt

### Semi-Drivable

- Dense vegetation
- Uneven terrain

### Non-Drivable

- Trees
- Rocks
- Bushes
- Structures

### Hazard

- Water
- Flooded terrain

---

## 3️⃣ Scene Understanding

The perception pipeline computes the percentage of each terrain category within the scene.

This enables robots to understand:

- Available drivable space
- Obstacle density
- Hazard coverage
- Terrain complexity

---

## 4️⃣ Navigation Recommendation

Based on terrain composition, the system generates navigation guidance such as:

- Safe to drive
- Reduce speed
- High obstacle density
- Hazard detected
- Route adjustment required

---

## 5️⃣ Visualization

The pipeline overlays terrain understanding onto the original RGB image, allowing developers to inspect perception quality and scene interpretation.

---

# 🖥 Visualization Results

The following figure illustrates the terrain understanding pipeline.

### Original RGB Image

Shows the outdoor environment captured by the robot.

### Semantic Segmentation

Displays pixel-wise terrain classification.

### Scene Understanding

Highlights drivable terrain, obstacles, and hazardous regions used for navigation decisions.

<img width="2048" height="853" alt="Terrain Scene Understanding" src="https://github.com/user-attachments/assets/26ca41a5-873c-4b0d-b05b-e86c952a3f04" />

---

# 📈 Representative Capabilities

The pipeline demonstrates:

- Semantic terrain understanding
- Drivable terrain extraction
- Obstacle identification
- Hazard detection
- Terrain distribution analysis
- Scene interpretation
- Navigation-aware perception
- Real-time visualization

---

# 🏗 Architecture

```text
RGB Image
      │
      ▼
Semantic Annotation
      │
      ▼
Terrain Classification
      │
      ▼
Scene Understanding
      │
      ▼
Hazard Detection
      │
      ▼
Terrain Statistics
      │
      ▼
Navigation Recommendation
```

---

# 🚀 Project Status

🟢 **Prototype**

### Current Features

- Semantic segmentation visualization
- Terrain classification
- Scene understanding
- Hazard detection
- Terrain statistics
- Navigation recommendations
- Visual debugging

### Planned Improvements

- Deep-learning semantic segmentation
- Real-time camera inference
- ROS 2 integration
- NVIDIA Isaac Sim integration
- Terrain traversability prediction
- Camera–LiDAR fusion
- Dynamic obstacle detection
- Terrain-aware path planning

---

# 📂 Repository Structure

```text
chore-terrain-scene-understanding/
│
├── src/
│   ├── RUGD_Data.py
│   └── RUGD_data2.py
│
├── assets/
│   ├── input/
│   ├── output/
│   └── examples/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
└── CITATION.cff
```

---

# ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/nimra-chorerobots/chore-terrain-scene-understanding.git

cd chore-terrain-scene-understanding
```

Install dependencies:

```bash
pip install -r requirements.txt
```

or

```bash
pip install numpy opencv-python matplotlib pillow
```

---

# 📦 Requirements

- Python 3.9+
- NumPy
- OpenCV
- Matplotlib
- Pillow

Example `requirements.txt`

```text
numpy
opencv-python
matplotlib
pillow
```

---

# ▶️ Running the Project

Run the terrain perception pipeline:

```bash
python src/RUGD_Data.py
```

or

```bash
python src/RUGD_data2.py
```

The pipeline performs the following steps:

1. Load RGB image
2. Load semantic annotation
3. Decode segmentation colors
4. Classify terrain categories
5. Compute terrain statistics
6. Detect hazards
7. Generate navigation recommendations
8. Visualize scene understanding

---

# 💡 Applications

This repository can be used for:

- Autonomous lawn robots
- Outdoor delivery robots
- Snow removal robots
- Agricultural robotics
- Mobile robotics
- Terrain perception research
- Semantic scene understanding
- Autonomous navigation
- Computer vision education
- Digital twin simulation

---

# 🔮 Future Work

Future versions of this repository will include:

- Deep-learning semantic segmentation
- YOLO-based terrain understanding
- Camera–LiDAR fusion
- ROS 2 perception nodes
- NVIDIA Isaac Sim integration
- Real-time deployment
- Traversability prediction
- Terrain-aware path planning
- Dynamic obstacle tracking

 
