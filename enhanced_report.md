# RHOAI 2.23 / OCP 4.18 Container Image Report

## Summary
- **Total Images**: 205 (125 infrastructure + 80 workload)
- **Registries**: quay.io (203), registry.redhat.io (2)
- **Base OS**: Unknown (135), RHEL9 (10), UBI9 (60)
- **Estimated Size**: ~20.5GB total download
- **Components**: 22 functional areas identified

## Component Overview
Component | Images (Unique) | Type | Description & Variants
--- | --- | --- | ---
Other Components | 34 (17 unique) | Other | Components that do not fit into predefin... | Variants: [RHEL9], [Py3.11, UBI9, pipeline], [Py3.12, UBI9, pipeline] (+14 more)
CUDA Notebooks | 28 (10 unique) | Cuda Notebooks | GPU-accelerated notebook environments wi... | Variants: [CUDA, notebook], [CUDA, notebook], [CUDA, notebook] (+7 more)
PyTorch Runtimes | 16 (8 unique) | Pytorch Runtimes | PyTorch runtime environments and serving... | Variants: [Py3.11, CUDA, UBI9, pipeline], [Py3.12, CUDA, UBI9, pipeline], [Py3.11, ROCm, UBI9, pipeline] (+5 more)
Generic Data Science Notebooks | 14 (5 unique) | Generic Data Science Notebooks | General-purpose data science notebook en... | Variants: [notebook], [notebook], [notebook] (+2 more)
Minimal Notebooks | 14 (5 unique) | Minimal Notebooks | Lightweight base notebook environments f... | Variants: [notebook], [notebook], [notebook] (+2 more)
PyTorch Notebooks | 14 (5 unique) | Pytorch Notebooks | PyTorch-optimized notebook environments ... | Variants: [notebook], [notebook], [notebook] (+2 more)
Code Server | 12 (5 unique) | Code Server | Web-based VS Code development environmen...
TensorFlow Runtimes | 12 (6 unique) | Tensorflow Runtimes | TensorFlow runtime environments and serv... | Variants: [Py3.11, CUDA, UBI9, pipeline], [Py3.12, CUDA, UBI9, pipeline], [Py3.11, ROCm, UBI9, pipeline] (+3 more)
TrustyAI Notebooks | 11 (4 unique) | Trustyai Notebooks | Notebook environments optimized for Trus... | Variants: [notebook], [notebook], [notebook] (+1 more)
Model Serving Infrastructure | 8 (4 unique) | Model Serving Infrastructure | Infrastructure for ML model deployment a...
Training | 8 (4 unique) | Training | Distributed training frameworks and util...
ROCm Notebooks | 6 (3 unique) | Rocm Notebooks | AMD ROCm-accelerated notebook environmen... | Variants: [ROCm, notebook], [ROCm, notebook], [ROCm, notebook]
vLLM | 6 (3 unique) | Vllm | High-performance LLM inference engine op...
CUDA Runtimes | 4 (2 unique) | Cuda Runtimes | NVIDIA CUDA runtime environments for GPU... | Variants: [Py3.11, CUDA, UBI9, workbench], [Py3.12, CUDA, UBI9, workbench]
Ray | 4 (2 unique) | Ray | Ray distributed computing framework for ...
Caikit NLP | 2 (1 unique) | Caikit Nlp | IBM Caikit framework for NLP model servi...
Caikit TGIS Serving | 2 (1 unique) | Caikit Tgis Serving | Caikit Text Generation Inference Server
TrustyAI Runtime | 2 (1 unique) | Trustyai Runtime | TrustyAI explainability and bias detecti...
OpenVINO | 2 (1 unique) | Openvino | Intel OpenVINO model serving and optimiz...
Text Generation Inference | 2 (1 unique) | Text Generation Inference | Optimized text generation inference serv...
FMS HuggingFace Tuning | 2 (1 unique) | Fms Hf Tuning | Foundation Model Stack HuggingFace fine-...
InstructLab | 2 (1 unique) | Instructlab | Red Hat InstructLab for large language m...

## Detailed Component Breakdown

### Infrastructure Components (125 images)

#### Other Components (30 images, 17 unique)
*Components that do not fit into predefined categories*

**Build Variants:**
- `sha256:a9892...` (RHEL9) [Sources: disconnected_helper]
- `sha256:43311...` (Python 3.11, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:cf650...` (Python 3.12, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:03ef7...` (Python 3.11, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:1ba6e...` (Python 3.12, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:2d73c...` (RHEL9) [Sources: disconnected_helper]
- `sha256:eed27...` (RHEL9) [Sources: disconnected_helper]
- `sha256:eadcd...` (Python 3.11, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:fda50...` (Python 3.12, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:a9bae...` (Python 3.11, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:9a8f2...` (Python 3.12, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:6c6f6...` (Python 3.11, ROCm, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:afe64...` (Python 3.12, ROCm, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:d0b2d...` (Python 3.11, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:38bb6...` (Python 3.12, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:5c10d...` [Sources: disconnected_helper]
- `sha256:d7e4a...` [Sources: disconnected_helper]

- quay.io/modh/odh-fms-guardrails-orchestrator-rhel9@sha256:a98926288a13f17484b61d7b86f315a51bafa51121ccc4e9bb7dd0870c580cb4
- quay.io/modh/odh-pipeline-runtime-datascience-cpu-py311-ubi9@sha256:4331121ffdf4aff725f8dc07bdd7a38744a4b61df977e3ebb61b73fe8dbd139d
- quay.io/modh/odh-pipeline-runtime-datascience-cpu-py312-ubi9@sha256:cf65016f50d27a3c7808fa6879f478d8b4f581a0a1221665860528d76425d59c
- ... and 27 more images

#### PyTorch Runtimes (16 images, 8 unique)
*PyTorch runtime environments and serving infrastructure*

**Build Variants:**
- `sha256:2072d...` (Python 3.11, CUDA, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:72ff2...` (Python 3.12, CUDA, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:35a5e...` (Python 3.11, ROCm, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:a3fd2...` (Python 3.12, ROCm, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:891ca...` (Python 3.11, CUDA, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:81945...` (Python 3.12, CUDA, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:bb928...` (Python 3.11, ROCm, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:8ac82...` (Python 3.12, ROCm, UBI9, Workbench) [Sources: disconnected_helper]

- quay.io/modh/odh-pipeline-runtime-pytorch-cuda-py311-ubi9@sha256:2072d38269c465aa7a3b6a849b2ea26eed0d9fef25f9fb3a0bd17ca422328818
- quay.io/modh/odh-pipeline-runtime-pytorch-cuda-py312-ubi9@sha256:72ff2381e5cb24d6f549534cb74309ed30e92c1ca80214669adb78ad30c5ae12
- quay.io/modh/odh-pipeline-runtime-pytorch-rocm-py311-ubi9@sha256:35a5eaff3d7152de67e968006d9012c87d8768f7e1e98906df76f550c53039b2
- ... and 13 more images

#### Generic Data Science Notebooks (14 images, 5 unique)
*General-purpose data science notebook environments*

**Build Variants:**
- `sha256:39853...` (Notebook) [Sources: disconnected_helper]
- `sha256:3e51c...` (Notebook) [Sources: disconnected_helper]
- `sha256:76e6a...` (Notebook) [Sources: disconnected_helper]
- `sha256:e2cab...` (Notebook) [Sources: disconnected_helper]
- `sha256:d0ba5...` (Notebook) [Sources: disconnected_helper]

- quay.io/modh/odh-generic-data-science-notebook@sha256:39853fd63555ebba097483c5ac6a375d6039e5522c7294684efb7966ba4bc693
- quay.io/modh/odh-generic-data-science-notebook@sha256:3e51c462fc03b5ccb080f006ced86d36480da036fa04b8685a3e4d6d51a817ba
- quay.io/modh/odh-generic-data-science-notebook@sha256:76e6af79c601a323f75a58e7005de0beac66b8cccc3d2b67efb6d11d85f0cfa1
- ... and 11 more images

#### Minimal Notebooks (14 images, 5 unique)
*Lightweight base notebook environments for development*

**Build Variants:**
- `sha256:39068...` (Notebook) [Sources: disconnected_helper]
- `sha256:4ba72...` (Notebook) [Sources: disconnected_helper]
- `sha256:e2296...` (Notebook) [Sources: disconnected_helper]
- `sha256:eec50...` (Notebook) [Sources: disconnected_helper]
- `sha256:2217d...` (Notebook) [Sources: disconnected_helper]

- quay.io/modh/odh-minimal-notebook-container@sha256:2217d8a9cbf84c2bd3e6c6dc09089559e8a3905687ca3739e897c4b45e2b00b3
- quay.io/modh/odh-minimal-notebook-container@sha256:39068767eebdf3a127fe8857fbdaca0832cdfef69eed6ec3ff6ed1858029420f
- quay.io/modh/odh-minimal-notebook-container@sha256:4ba72ae7f367a36030470fa4ac22eca0aab285c7c3f1c4cdcc33dc07aa522143
- ... and 11 more images

#### PyTorch Notebooks (14 images, 5 unique)
*PyTorch-optimized notebook environments for deep learning*

**Build Variants:**
- `sha256:2403b...` (Notebook) [Sources: disconnected_helper]
- `sha256:806e6...` (Notebook) [Sources: disconnected_helper]
- `sha256:97b34...` (Notebook) [Sources: disconnected_helper]
- `sha256:b68e0...` (Notebook) [Sources: disconnected_helper]
- `sha256:20f7a...` (Notebook) [Sources: disconnected_helper]

- quay.io/modh/odh-pytorch-notebook@sha256:20f7ab8e7954106ea5e22f3ee0ba8bc7b03975e5735049a765e021aa7eb06861
- quay.io/modh/odh-pytorch-notebook@sha256:2403b3dccc3daf5b45a973c49331fdac4ec66e2e020597975fcd9cb4a625099b
- quay.io/modh/odh-pytorch-notebook@sha256:806e6524cb46bcbd228e37a92191c936bb4c117100fc731604e19df80286b19d
- ... and 11 more images

#### Code Server (4 images, 5 unique)
*Web-based VS Code development environments*

**Build Variants:**
- `sha256:1fd51...` [Sources: disconnected_helper]
- `sha256:b1a04...` [Sources: disconnected_helper]
- `sha256:92f2a...` [Sources: disconnected_helper]
- `sha256:da2ee...` (Python 3.11, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:3043c...` (Python 3.12, UBI9, Workbench) [Sources: disconnected_helper]

- quay.io/modh/odh-workbench-codeserver-datascience-cpu-py311-ubi9@sha256:da2ee865eeb8f69ec3d05893f8b1a02942671a573541e92d759eef152b540c53
- quay.io/modh/odh-workbench-codeserver-datascience-cpu-py312-ubi9@sha256:3043cdd56e62160c1dfbb93f3de6c08432fd805e771a53513b317c9cb4787999
- quay.io/modh/odh-workbench-codeserver-datascience-cpu-py311-ubi9@sha256:da2ee865eeb8f69ec3d05893f8b1a02942671a573541e92d759eef152b540c53
- ... and 1 more images

#### TensorFlow Runtimes (12 images, 6 unique)
*TensorFlow runtime environments and serving infrastructure*

**Build Variants:**
- `sha256:0549a...` (Python 3.11, CUDA, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:5a737...` (Python 3.12, CUDA, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:dfe20...` (Python 3.11, ROCm, UBI9, Pipeline) [Sources: disconnected_helper]
- `sha256:fdbe1...` (Python 3.11, CUDA, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:3d21b...` (Python 3.12, CUDA, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:b7ca9...` (Python 3.11, ROCm, UBI9, Workbench) [Sources: disconnected_helper]

- quay.io/modh/odh-pipeline-runtime-tensorflow-cuda-py311-ubi9@sha256:0549a243b910ba0b900d3ffc45614a1cff0ff61caa31258e051bc357c8b53b92
- quay.io/modh/odh-pipeline-runtime-tensorflow-cuda-py312-ubi9@sha256:5a737f9057f07100286e6b584fe54fa4611d91bef5eb77b172181e7a9a4214e3
- quay.io/modh/odh-pipeline-runtime-tensorflow-rocm-py311-ubi9@sha256:dfe20c15324f2267a267e1edf206ea31ca083381a1cee72f377ff475f37fe5a4
- ... and 9 more images

#### TrustyAI Notebooks (11 images, 4 unique)
*Notebook environments optimized for TrustyAI workflows*

**Build Variants:**
- `sha256:70fe4...` (Notebook) [Sources: disconnected_helper]
- `sha256:8c5e6...` (Notebook) [Sources: disconnected_helper]
- `sha256:fe883...` (Notebook) [Sources: disconnected_helper]
- `sha256:a1b86...` (Notebook) [Sources: disconnected_helper]

- quay.io/modh/odh-trustyai-notebook@sha256:70fe49cee6d5a231ddea7f94d7e21aefd3d8da71b69321f51c406a92173d3334
- quay.io/modh/odh-trustyai-notebook@sha256:8c5e653f6bc6a2050565cf92f397991fbec952dc05cdfea74b65b8fd3047c9d4
- quay.io/modh/odh-trustyai-notebook@sha256:a1b863c2787ba2bca292e381561ed1d92cf5bc25705edfb1ded5e0720a12d102
- ... and 8 more images

#### Model Serving Infrastructure (2 images, 4 unique)
*Infrastructure for ML model deployment and serving*

**Build Variants:**
- `sha256:149ae...` [Sources: disconnected_helper]
- `sha256:3d9d2...` [Sources: disconnected_helper]
- `sha256:b5570...` [Sources: disconnected_helper]
- `sha256:c3c4c...` [Sources: disconnected_helper]

- quay.io/modh/kserve-controller@sha256:3d9d27b6a836d1eb0eff993701cafd1b0e22c39ed26377f512c30702abd40ebd
- quay.io/modh/kserve-controller@sha256:3d9d27b6a836d1eb0eff993701cafd1b0e22c39ed26377f512c30702abd40ebd

#### CUDA Runtimes (4 images, 2 unique)
*NVIDIA CUDA runtime environments for GPU acceleration*

**Build Variants:**
- `sha256:be2e6...` (Python 3.11, CUDA, UBI9, Workbench) [Sources: disconnected_helper]
- `sha256:f7126...` (Python 3.12, CUDA, UBI9, Workbench) [Sources: disconnected_helper]

- quay.io/modh/odh-workbench-jupyter-minimal-cuda-py311-ubi9@sha256:be2e684666d17f2555d7956b61d842f3fc8516d5bea0cbec221300ca7eb8ced1
- quay.io/modh/odh-workbench-jupyter-minimal-cuda-py312-ubi9@sha256:f7126e237f1dfe3a4cda89b60c4e8d9e45afabb247030765edb1c5532a7010fc
- quay.io/modh/odh-workbench-jupyter-minimal-cuda-py311-ubi9@sha256:be2e684666d17f2555d7956b61d842f3fc8516d5bea0cbec221300ca7eb8ced1
- ... and 1 more images

#### TrustyAI Runtime (2 images, 1 unique)
*TrustyAI explainability and bias detection runtime*

- quay.io/modh/odh-trustyai-hf-detector-runtime-rhel9@sha256:21bb5f9980e516fccdf6a2fa4fbb259cb4f54b9cd42abf499f2b0c911e9433c9
- quay.io/modh/odh-trustyai-hf-detector-runtime-rhel9@sha256:21bb5f9980e516fccdf6a2fa4fbb259cb4f54b9cd42abf499f2b0c911e9433c9

#### InstructLab (2 images, 1 unique)
*Red Hat InstructLab for large language model training*

- registry.redhat.io/rhelai1/instructlab-nvidia-rhel9@sha256:b3dc9af0244aa6b84e6c3ef53e714a316daaefaae67e28de397cd71ee4b2ac7e
- registry.redhat.io/rhelai1/instructlab-nvidia-rhel9@sha256:b3dc9af0244aa6b84e6c3ef53e714a316daaefaae67e28de397cd71ee4b2ac7e


### Workload Components (80 images)

#### Other Components (4 images, 17 unique)
*Components that do not fit into predefined categories*

**Build Variants:**
- `sha256:a9892...` (RHEL9) [Sources: disconnected_helper] (2 refs)
- `sha256:43311...` (Python 3.11, UBI9, Pipeline) [Sources: disconnected_helper] (2 refs)
- `sha256:cf650...` (Python 3.12, UBI9, Pipeline) [Sources: disconnected_helper] (2 refs)
- `sha256:03ef7...` (Python 3.11, UBI9, Pipeline) [Sources: disconnected_helper] (2 refs)
- `sha256:1ba6e...` (Python 3.12, UBI9, Pipeline) [Sources: disconnected_helper] (2 refs)
- `sha256:2d73c...` (RHEL9) [Sources: disconnected_helper] (2 refs)
- `sha256:eed27...` (RHEL9) [Sources: disconnected_helper] (2 refs)
- `sha256:eadcd...` (Python 3.11, UBI9, Workbench) [Sources: disconnected_helper] (2 refs)
- `sha256:fda50...` (Python 3.12, UBI9, Workbench) [Sources: disconnected_helper] (2 refs)
- `sha256:a9bae...` (Python 3.11, UBI9, Workbench) [Sources: disconnected_helper] (2 refs)
- `sha256:9a8f2...` (Python 3.12, UBI9, Workbench) [Sources: disconnected_helper] (2 refs)
- `sha256:6c6f6...` (Python 3.11, ROCm, UBI9, Workbench) [Sources: disconnected_helper] (2 refs)
- `sha256:afe64...` (Python 3.12, ROCm, UBI9, Workbench) [Sources: disconnected_helper] (2 refs)
- `sha256:d0b2d...` (Python 3.11, UBI9, Workbench) [Sources: disconnected_helper] (2 refs)
- `sha256:38bb6...` (Python 3.12, UBI9, Workbench) [Sources: disconnected_helper] (2 refs)
- `sha256:5c10d...` [Sources: disconnected_helper] (2 refs)
- `sha256:d7e4a...` [Sources: disconnected_helper] (2 refs)

- quay.io/modh/ta-lmes-driver@sha256:5c10dc5db0e294fd63447f23aa55308e36891299b4ce7beed67651ff52c3ab91
- quay.io/modh/ta-lmes-job@sha256:d7e4a8cbf421d71c0f48b20b49f9e47d9b91e5d95c5fe9d3da8f4ff233c06459
- ... and 2 more images

#### CUDA Notebooks (28 images, 10 unique)
*GPU-accelerated notebook environments with CUDA support*

**Build Variants:**
- `sha256:00c53...` (CUDA, Notebook) [Sources: disconnected_helper] (3 refs)
- `sha256:0e57a...` (CUDA, Notebook) [Sources: disconnected_helper] (3 refs)
- `sha256:3da74...` (CUDA, Notebook) [Sources: disconnected_helper] (3 refs)
- `sha256:6fade...` (CUDA, Notebook) [Sources: disconnected_helper] (3 refs)
- `sha256:81484...` (CUDA, Notebook) [Sources: disconnected_helper] (3 refs)
- `sha256:88d80...` (CUDA, Notebook) [Sources: disconnected_helper] (3 refs)
- `sha256:a484d...` (CUDA, Notebook) [Sources: disconnected_helper] (3 refs)
- `sha256:f6cdc...` (CUDA, Notebook) [Sources: disconnected_helper] (3 refs)
- `sha256:55598...` (CUDA, Notebook) [Sources: disconnected_helper] (2 refs)
- `sha256:99d3f...` (CUDA, Notebook) [Sources: disconnected_helper] (2 refs)

- quay.io/modh/cuda-notebooks@sha256:00c53599f5085beedd0debb062652a1856b19921ccf59bd76134471d24c3fa7d
- quay.io/modh/cuda-notebooks@sha256:0e57a0b756872636489ccd713dc9f00ad69d0c481a66ee0de97860f13b4fedcd
- ... and 26 more images

#### Code Server (8 images, 5 unique)
*Web-based VS Code development environments*

**Build Variants:**
- `sha256:1fd51...` [Sources: disconnected_helper] (3 refs)
- `sha256:b1a04...` [Sources: disconnected_helper] (3 refs)
- `sha256:92f2a...` [Sources: disconnected_helper] (2 refs)
- `sha256:da2ee...` (Python 3.11, UBI9, Workbench) [Sources: disconnected_helper] (2 refs)
- `sha256:3043c...` (Python 3.12, UBI9, Workbench) [Sources: disconnected_helper] (2 refs)

- quay.io/modh/codeserver@sha256:1fd51b0e8a14995f1f7273a4b0b40f6e7e27e225ab179959747846e54079d61e
- quay.io/modh/codeserver@sha256:92f2a10dde5c96b29324426b4325401e8f4a0d257e439927172d5fe909289c44
- ... and 6 more images

#### Model Serving Infrastructure (6 images, 4 unique)
*Infrastructure for ML model deployment and serving*

**Build Variants:**
- `sha256:149ae...` [Sources: disconnected_helper] (2 refs)
- `sha256:3d9d2...` [Sources: disconnected_helper] (2 refs)
- `sha256:b5570...` [Sources: disconnected_helper] (2 refs)
- `sha256:c3c4c...` [Sources: disconnected_helper] (2 refs)

- quay.io/modh/kserve-agent@sha256:149aeaabab78c94773ded2469537d444bbd73d2f705ab20f6b3ef75238a7fea2
- quay.io/modh/kserve-router@sha256:b5570dd240aca81d7e86e874d82917ba852afc4e7975cbb00cde19c58e6456dd
- ... and 4 more images

#### Training (8 images, 4 unique)
*Distributed training frameworks and utilities*

**Build Variants:**
- `sha256:f64f7...` [Sources: disconnected_helper] (2 refs)
- `sha256:1d0ca...` [Sources: disconnected_helper] (2 refs)
- `sha256:88373...` [Sources: disconnected_helper] (2 refs)
- `sha256:6cdae...` [Sources: disconnected_helper] (2 refs)

- quay.io/modh/training@sha256:f64f7bba3f1020d39491ac84d40d362a52e4822bdc11a33cfff021178b7c4097
- quay.io/modh/training@sha256:1d0caea3e5d56ff7d672954b1ad511e661df9bdb364d56879961169a4ca8dae0
- ... and 6 more images

#### ROCm Notebooks (6 images, 3 unique)
*AMD ROCm-accelerated notebook environments*

**Build Variants:**
- `sha256:19936...` (ROCm, Notebook) [Sources: disconnected_helper] (2 refs)
- `sha256:1f0b1...` (ROCm, Notebook) [Sources: disconnected_helper] (2 refs)
- `sha256:f9470...` (ROCm, Notebook) [Sources: disconnected_helper] (2 refs)

- quay.io/modh/rocm-notebooks@sha256:199367d2946fc8427611b4b96071cb411433ffbb5f0988279b10150020af22db
- quay.io/modh/rocm-notebooks@sha256:1f0b19b7ae587d638e78697c67f1290d044e48bfecccfb72d7a16faeba13f980
- ... and 4 more images

#### vLLM (6 images, 3 unique)
*High-performance LLM inference engine optimized for throughput*

**Build Variants:**
- `sha256:39343...` [Sources: disconnected_helper] (2 refs)
- `sha256:bf843...` [Sources: disconnected_helper] (2 refs)
- `sha256:db766...` [Sources: disconnected_helper] (2 refs)

- quay.io/modh/vllm@sha256:3934334c8270789a08f0b40a7a54cc712864fff0838ac2990a3b5711e175eef5
- quay.io/modh/vllm@sha256:bf8437d698f91ce8127dd2ea43b2bd01091d567fc49cc9b99bd56bea27cfdc45
- ... and 4 more images

#### Ray (4 images, 2 unique)
*Ray distributed computing framework for ML workloads*

**Build Variants:**
- `sha256:6d076...` [Sources: disconnected_helper] (2 refs)
- `sha256:60916...` [Sources: disconnected_helper] (2 refs)

- quay.io/modh/ray@sha256:6d076aeb38ab3c34a6a2ef0f58dc667089aa15826fa08a73273c629333e12f1e
- quay.io/modh/ray@sha256:6091617d45d5681058abecda57e0ee33f57b8855618e2509f1a354a20cc3403c
- ... and 2 more images

#### Caikit NLP (2 images, 1 unique)
*IBM Caikit framework for NLP model serving*

- quay.io/modh/caikit-nlp@sha256:5365ab0ef8f8d032a9f6f02970f3adb5512641c2e340876fa8bd66d82f98c82c
- quay.io/modh/caikit-nlp@sha256:5365ab0ef8f8d032a9f6f02970f3adb5512641c2e340876fa8bd66d82f98c82c

#### Caikit TGIS Serving (2 images, 1 unique)
*Caikit Text Generation Inference Server*

- quay.io/modh/caikit-tgis-serving@sha256:776c54dd8a9b968de979211f2513b961d63c9272bf41aae0ef26e62851c52570
- quay.io/modh/caikit-tgis-serving@sha256:776c54dd8a9b968de979211f2513b961d63c9272bf41aae0ef26e62851c52570

#### OpenVINO (2 images, 1 unique)
*Intel OpenVINO model serving and optimization toolkit*

- quay.io/modh/openvino_model_server@sha256:9b3db0c5f9717ebe57af64c54e7a18dc65ebef25c275a61c2960a2b409d21a42
- quay.io/modh/openvino_model_server@sha256:9b3db0c5f9717ebe57af64c54e7a18dc65ebef25c275a61c2960a2b409d21a42

#### Text Generation Inference (2 images, 1 unique)
*Optimized text generation inference server*

- quay.io/modh/text-generation-inference@sha256:850039122ab37c709fe4b9000c0617d2d163d5ab877e56aa611338f5911e5e8c
- quay.io/modh/text-generation-inference@sha256:850039122ab37c709fe4b9000c0617d2d163d5ab877e56aa611338f5911e5e8c

#### FMS HuggingFace Tuning (2 images, 1 unique)
*Foundation Model Stack HuggingFace fine-tuning framework*

- quay.io/modh/fms-hf-tuning@sha256:1ad46fe1a23f41f190c49ec2549c64f484c88fe220888a7a5700dd857ca243cc
- quay.io/modh/fms-hf-tuning@sha256:1ad46fe1a23f41f190c49ec2549c64f484c88fe220888a7a5700dd857ca243cc



## Security Analysis

### Registry Distribution
- **Trusted Red Hat**: 2 images (1.0%)
- **Community/Other**: 203 images (99.0%)

### Registry Breakdown
Registry | Images | Percentage | Trust Level
--- | --- | --- | ---
quay.io | 203 | 99.0% | Community
registry.redhat.io | 2 | 1.0% | Trusted

### Recommendations
- Consider migrating community images to trusted registries
