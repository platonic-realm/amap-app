# AMAP Application

AMAP-APP is a desktop application that leverages deep learning to perform [segmentation and morphometry quantification of fluorescent microscopy images of podocytes](https://www.kidney-international.org/article/S0085-2538(23)00180-1/fulltext). The application runs comfortably on the CPU; a GPU is **optional** and, when available, can accelerate inference (toggled per project).

![AMAP Results](res/images/header.png)
<!-- IMAGE: top banner / hero image. Existing file res/images/header.png is reused. Replace if you want an updated banner. -->

This application is a reimplementation of the [original research](https://github.com/bozeklab/amap) with modifications to the instance segmentation algorithm aimed at improving CPU efficiency. A notable departure from the original methodology is in the instance segmentation, which no longer depends on pixel-embedding clustering. Instead, it uses PyTorch operations and a Connected Component Labeling algorithm to achieve comparable results.

AMAP-APP is a cross-platform application implemented in Python 3.9, primarily tested on Linux and with less extensive testing on Windows and Mac. While some visual inconsistencies may arise between platforms, these variations do not compromise the functionality of the application.

## Requirements

#### Software
A full list of required packages is available in [requirements.txt](./requirements.txt), but to name the major dependencies:

* [PySide6](https://pypi.org/project/PySide6/) — Python bindings for the Qt framework, used for the user interface.
* [PyTorch](https://pytorch.org/) — inference (and training) of the deep learning models.
* [tifffile](https://pypi.org/project/tifffile/) — reading data samples in TIFF format.
* [OpenCV](https://pypi.org/project/opencv-python/), [NumPy](https://numpy.org/), [scikit-image](https://scikit-image.org/) and [SciPy](https://scipy.org/) — image processing and morphometry.
* [pandas](https://pandas.pydata.org/) — assembling the morphometry result tables.

#### Hardware

* **Minimum:** 4 GB of RAM and 2 CPU cores.
* **Recommended:** 16 GB of RAM and 8 CPU cores.
* **Optional:** a CUDA-capable NVIDIA GPU. Inference will use it automatically when the *Use GPU* option is enabled and a compatible GPU is detected; otherwise AMAP-APP runs on the CPU.

## Installation

1. Make sure you have the tools below installed
    * git
    * Python 3.9

2. Clone the repository
```bash
git clone https://github.com/bozeklab/amap-app.git
```

3. Prepare the Python environment

Go into the **amap-app** directory

```bash
cd amap-app
```

Create a virtual environment

```bash
python -m venv venv
```
Activate the virtual environment

* On Linux/Mac

```bash
source ./venv/bin/activate
```

* On Windows

```powershell
Set-ExecutionPolicy Unrestricted -Scope Process
.\venv\Scripts\Activate
```

Install the requirements

* On Linux/Mac

```bash
pip install -r requirements.txt
```

* On Windows

```powershell
pip install -r requirements-win.txt
```

## Update

To update AMAP to the latest version:

* Open a terminal in the amap-app directory

* Run the command:

```bash
git pull
```

## Running AMAP-APP

Activate the virtual environment before launching the application. First, using a terminal or PowerShell, go to the repository's directory.

Activate the virtual environment

* On Linux/Mac

```bash
source ./venv/bin/activate
```

* On Windows

```powershell
Set-ExecutionPolicy Unrestricted -Scope Process
.\venv\Scripts\Activate
```

Execute the application

```bash
python main.py
```

## Using AMAP-APP

AMAP processes images in batches. A **project** is a batch of images together with its configuration. All images in a project must share the same order of dimensionality. AMAP currently supports TIFF files only.

### 1. Create a project

* Click the **Add** button.

<p align="center"><img src="res/images/add_button.jpg" alt="Add Project" width="500"/></p>
<!-- IMAGE: the project list with the "Add" / "Remove" buttons highlighted. Existing file res/images/add_button.jpg is reused; update if the button labels/positions changed. -->

* Select the directory that contains the TIFF files. AMAP copies the images into a new project folder under `projects/`.

<p align="center"><img src="res/images/select_project.jpg" alt="Select Project" width="500"/></p>
<!-- IMAGE: the OS directory-picker dialog. Existing file res/images/select_project.jpg is reused. -->

### 2. Configure the project

Select the project in the list to enable its settings. The settings are split into resource sliders (left) and model/data options (right).

<p align="center"><img src="res/images/configure_project.jpg" alt="Configure Project" width="500"/></p>
<!-- IMAGE (NEEDS UPDATING): a current screenshot of the configuration panel. The existing res/images/configure_project.jpg is OUT OF DATE — it predates the value labels under each slider, the "Data-loader workers" slider, the "Model checkpoint" dropdown, and the "Use GPU" checkbox. Capture a fresh screenshot of the bottom panel with a project selected and overwrite res/images/configure_project.jpg. -->

**Resource sliders** (each shows the concrete value it maps to in a small label beneath it):

* **CPU allocation** — Share of logical CPU cores used for inference, in five steps from ~20% up to 100% of the cores. The label shows the resulting percentage and thread count (e.g. `80% · 10 threads`).
* **Memory allocation** — Controls the inference batch size; larger batches are faster but use more RAM. The label shows the batch size (e.g. `batch size 24`). Roughly 2 GB of RAM suffices for the lowest setting; 8 GB or more is advised for the highest.
* **Data-loader workers** — Number of background processes that read and prepare image patches in parallel. A value is suggested automatically from the CPU and Memory sliders (and capped at half the logical cores so the loaders don't compete with the inference threads), but you can override it; moving the CPU or Memory slider re-suggests a value. The label shows the worker count (e.g. `6 workers`). `0` loads data in the main process.

**Model and data options:**

* **Model checkpoint** — Selects the trained model weights. AMAP-APP ships with `cp_10940.pth` (default) and an additional checkpoint trained for IgA Nephropathy, `cp_12940.pth`. Any `.pth` file placed in `res/model/` appears in this list.
* **Target channel** — AMAP tries to detect the relevant channel automatically; adjust this only if the automatic detection is wrong.
* **Stacked** — Whether the input is a stack of images. If so, AMAP uses a maximum projection of the stack. Change this only if the automatic detection is wrong.
* **Old ROI algorithm (AMAP)** — Use the original AMAP ROI detection instead of the AMAP-APP method. Leave unchecked for the AMAP-APP algorithm.
* **SD length analysis** — Enables slit-diaphragm length analysis in the morphometry results. Enabling it shows a confirmation dialog. **Important:** this feature may conflict with a patent filed after the AMAP paper was published. Users are solely responsible for ensuring compliance with all applicable intellectual-property regulations and legal requirements.
* **Use GPU** — When enabled and a CUDA-capable GPU is available, inference runs on the GPU; otherwise it falls back to the CPU. Disable to force CPU execution.

### 3. Run the analysis

* Click **Start** and wait for processing to finish. Segmentation runs first, followed by morphometry; a progress dialog reports the status. You can press **Stop** to cancel.

<p align="center"><img src="res/images/progress.jpg" alt="Progress" width="500"/></p>
<!-- IMAGE: the progress dialog during processing. Existing file res/images/progress.jpg is reused. -->

### 4. View the results

* Use the **Segmentation** and **Morphometry** buttons to open the output folders. Segmentation results (instance, semantic, ROI and a combined preview, plus the raw `.npy` predictions) and the morphometry CSV tables are written under the project folder.

<p align="center"><img src="res/images/results.jpg" alt="Results" width="500"/></p>
<!-- IMAGE: the "Results" row with the Segmentation / Morphometry buttons, ideally next to an example output. Existing file res/images/results.jpg is reused. -->
