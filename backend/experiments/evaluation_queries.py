# Dictionaries representing evaluation pairs.
# Types:
#   - Key: query, Value: 1 document
#       - easy
#       - intermediate
#       - difficult
#       - trap
#   - Key: query, Value: 2 documents
#   - Key: query, Value: None
#       - easy
#       - intermediate
#       - difficult


# ----------------------------------------
#          QUERY - 1 DOCUMENT
# ----------------------------------------
queries_easy = {
    "GDPR compliance and neuroimaging data privacy": "2026-01-05_Alice-Robertson_Compliance-Review.pdf",
    "bottleneck fusion for multimodal medical data integration": "2026-01-08_Chloe-Nguyen_Multimodal-Fusion-Logic.pdf",
    "mandatory clinical metrics for alzheimers disease classification": "2026-01-12_Alice-Robertson_Evaluation-Standards.pdf",
    "tau protein biomarkers and hippocampal atrophy correlation": "2026-01-14_Bob-Martinez_Proteomics-Integration.pdf",
    "hyperparameter sweep and weights and biases tracking": "2026-01-16_Chloe-Nguyen_Hyperparameter-Sweep.pdf",
    "docker environment setup for local hardware clusters": "2026-01-18_Daniel-Fischer_Environment-Setup.pdf",
    "synthetic data generation and smote for class imbalance": "2026-01-22_Bob-Martinez_Synthetic-Data-Gen.pdf",
    "weekly team sync and tau protein data audit": "2026-01-27_Daniel-Fischer_Weekly-Sync.pdf",
    "scaled dot product attention mechanism": "2025-11-10_Chloe-Nguyen_Attention-Is-All-You-Need.pdf",
    "deep residual learning for image recognition": "2025-11-12_Chloe-Nguyen_Deep-Residual-Learning-for-Image-Recognition.pdf",
    "vision transformer using image patches": "2025-11-15_Chloe-Nguyen_An-Image-is-Worth-16x16-Words-Transformers-for-Image-Recognition-at-Scale.pdf",
    "retrieval augmented generation for nlp tasks": "2025-11-20_Chloe-Nguyen_Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.pdf",
    "adam optimizer for stochastic optimization": "2025-11-22_Chloe-Nguyen_Adam-A-Method-for-Stochastic-Optimization.pdf",
    "taxonomy of multimodal machine learning": "2025-11-05_Alice-Robertson_Multimodal-Machine-Learning-A-Survey-and-Taxonomy.pdf",
    "pathological network model for alzheimers interventions": "2025-11-26_Alice-Robertson_A-Systemic-Pathological-Network-Model-and-Combinatorial-Intervention-Strategies-for-Alzheimers-Disease.pdf",
    "graph model of tau pathology spreading": "2025-11-29_Bob-Martinez_A-single-snapshot-inverse-solver-for-two-species-graph-model-of-tau-pathology-spreading-in-human-Alzheimer-disea.pdf",
    "personalized trajectories of cortical atrophy": "2025-12-02_Bob-Martinez_Data-driven-spatiotemporal-modeling-reveals-personalized-trajectories-of-cortical-atrophy-in-Alzheimers-disease.pdf",
    "pathology steered stratification for subtype identification": "2025-12-04_Alice-Robertson_Pathology-Steered-Stratification-Network-for-Subtype-Identification-in-Alzheimers-Disease.pdf",
    "video reasoning over traffic events benchmark": "2025-12-05_Bob-Martinez_SUTD-TrafficQA-A-Question-Answering-Benchmark-and-an-Efficient-Network-for-Video-Reasoning-over-Traffic-Events.pdf",
    "deep counterfactuals for alzheimers prediction": "2025-12-07_Bob-Martinez_A-Quantitatively-Interpretable-Model-for-Alzheimers-Disease-Prediction-Using-Deep-Counterfactuals.pdf",
    "multimodal attention for disease diagnosis": "2025-12-08_Chloe-Nguyen_Multimodal-Attention-based-Deep-Learning-for-Alzheimers-Disease-Diagnosis.pdf",
    "evaluating disease focus in deep learning models": "2025-12-10_Alice-Robertson_A-Quantitative-Approach-for-Evaluating-Disease-Focus-and-Interpretability-of-Deep-Learning-Models-for-Alzheimers.pdf",
    "explainable ai requirements for clinicians": "2025-12-12_Chloe-Nguyen_Exploring-the-Requirements-of-Clinicians-for-Explainable-AI-Decision-Support-Systems-in-Intensive-Care.pdf",
    "transfer learning for 3d medical image analysis": "2025-12-14_Bob-Martinez_Med3D-Transfer-Learning-for-3D-Medical-Image-Analysis.pdf",
    "generative adversarial networks in medical imaging review": "2025-12-16_Chloe-Nguyen_Generative-Adversarial-Network-in-Medical-Imaging-A-Review.pdf",
    "success factors for scientific teams": "2025-12-20_Daniel-Fischer_Freshness-Persistence-and-Success-of-Scientific-Teams.pdf",
    "monetary value of large scientific collaboration": "2025-12-22_Daniel-Fischer_The-Link-Between-Large-Scientific-Collaboration-and-Productivity-Rethinking-How-to-Estimate-the-Monetary-Value-o.pdf",
    "researcher perceptions of llm tools": "2025-12-24_Daniel-Fischer_LLMs-as-Research-Tools-A-Large-Scale-Survey-of-Researchers-Usage-and-Perceptions.pdf"
}

queries_intermediate = {
    "distinction between pseudonymization and anonymization under gdpr": "2026-01-05_Alice-Robertson_Compliance-Review.pdf",
    "kl divergence for latent space regularization": "2026-01-08_Chloe-Nguyen_Multimodal-Fusion-Logic.pdf",
    "area under the precision recall curve for imbalanced data": "2026-01-12_Alice-Robertson_Evaluation-Standards.pdf",
    "k-nearest neighbors imputation for missing tau protein values": "2026-01-14_Bob-Martinez_Proteomics-Integration.pdf",
    "optimal batch size and learning rate interaction in adamw": "2026-01-16_Chloe-Nguyen_Hyperparameter-Sweep.pdf",
    "solving numpy and scipy version mismatch for linear algebra": "2026-01-18_Daniel-Fischer_Environment-Setup.pdf",
    "elastic transformations for simulating anatomical variability": "2026-01-22_Bob-Martinez_Synthetic-Data-Gen.pdf",
    "dynamic masking for incomplete multimodal inputs": "2026-01-27_Daniel-Fischer_Weekly-Sync.pdf",
    "multi-head self-attention and position-wise feed-forward networks": "2025-11-10_Chloe-Nguyen_Attention-Is-All-You-Need.pdf",
    "shortcut connections and identity mapping for optimization": "2025-11-12_Chloe-Nguyen_Deep-Residual-Learning-for-Image-Recognition.pdf",
    "transformer encoder blocks for fine-grained image recognition": "2025-11-15_Chloe-Nguyen_An-Image-is-Worth-16x16-Words-Transformers-for-Image-Recognition-at-Scale.pdf",
    "knowledge-intensive tasks using dense vector retrieval": "2025-11-20_Chloe-Nguyen_Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.pdf",
    "adaptive moment estimation mechanics for deep learning": "2025-11-22_Chloe-Nguyen_Adam-A-Method-for-Stochastic-Optimization.pdf",
    "challenges in cross-modal alignment and feature fusion": "2025-11-05_Alice-Robertson_Multimodal-Machine-Learning-A-Survey-and-Taxonomy.pdf",
    "combinatorial intervention strategies for alzheimers networks": "2025-11-26_Alice-Robertson_A-Systemic-Pathological-Network-Model-and-Combinatorial-Intervention-Strategies-for-Alzheimers-Disease.pdf",
    "snapshot inverse solver for two-species graph models": "2025-11-29_Bob-Martinez_A-single-snapshot-inverse-solver-for-two-species-graph-model-of-tau-pathology-spreading-in-human-Alzheimer-disea.pdf",
    "spatiotemporal modeling of cortical atrophy trajectories": "2025-12-02_Bob-Martinez_Data-driven-spatiotemporal-modeling-reveals-personalized-trajectories-of-cortical-atrophy-in-Alzheimers-disease.pdf",
    "subtype identification in alzheimers using stratification networks": "2025-12-04_Alice-Robertson_Pathology-Steered-Stratification-Network-for-Subtype-Identification-in-Alzheimers-Disease.pdf",
    "efficient networks for temporal reasoning in video": "2025-12-05_Bob-Martinez_SUTD-TrafficQA-A-Question-Answering-Benchmark-and-an-Efficient-Network-for-Video-Reasoning-over-Traffic-Events.pdf",
    "interpretable volumetric changes using deep counterfactuals": "2025-12-07_Bob-Martinez_A-Quantitatively-Interpretable-Model-for-Alzheimers-Disease-Prediction-Using-Deep-Counterfactuals.pdf",
    "attention weights for integrating imaging and clinical data": "2025-12-08_Chloe-Nguyen_Multimodal-Attention-based-Deep-Learning-for-Alzheimers-Disease-Diagnosis.pdf",
    "quantitative metrics for disease focus and saliency maps": "2025-12-10_Alice-Robertson_A-Quantitative-Approach-for-Evaluating-Disease-Focus-and-Interpretability-of-Deep-Learning-Models-for-Alzheimers.pdf",
    "clinical requirements for explainable ai decision support": "2025-12-12_Chloe-Nguyen_Exploring-the-Requirements-of-Clinicians-for-Explainable-AI-Decision-Support-Systems-in-Intensive-Care.pdf",
    "3d medical imaging analysis using pre-trained med3d models": "2025-12-14_Bob-Martinez_Med3D-Transfer-Learning-for-3D-Medical-Image-Analysis.pdf",
    "gan applications for medical image synthesis and denoising": "2025-12-16_Chloe-Nguyen_Generative-Adversarial-Network-in-Medical-Imaging-A-Review.pdf",
    "link between scientific team freshness and success": "2025-12-20_Daniel-Fischer_Freshness-Persistence-and-Success-of-Scientific-Teams.pdf",
    "productivity estimates of large scale scientific collaborations": "2025-12-22_Daniel-Fischer_The-Link-Between-Large-Scientific-Collaboration-and-Productivity-Rethinking-How-to-Estimate-the-Monetary-Value-o.pdf",
    "large scale survey of researcher usage of llms": "2025-12-24_Daniel-Fischer_LLMs-as-Research-Tools-A-Large-Scale-Survey-of-Researchers-Usage-and-Perceptions.pdf"
}

queries_difficult = {
    "unauthorized data transfer to neurocloud analytic solutions": "2026-01-05_Alice-Robertson_Compliance-Review.pdf",
    "intermediate fusion vs early fusion for 3d mri data": "2026-01-08_Chloe-Nguyen_Multimodal-Fusion-Logic.pdf",
    "mandatory external validation using oasis-3 dataset": "2026-01-12_Alice-Robertson_Evaluation-Standards.pdf",
    "missing tau protein data for subjects ad-102 to ad-118": "2026-01-14_Bob-Martinez_Proteomics-Integration.pdf",
    "mri encoder overfitting patterns starting at epoch 50": "2026-01-16_Chloe-Nguyen_Hyperparameter-Sweep.pdf",
    "cuda 12.1 and pytorch 2.4.0 cluster requirements": "2026-01-18_Daniel-Fischer_Environment-Setup.pdf",
    "parameters for bob's elastic transform alpha 50 and sigma 8": "2026-01-22_Bob-Martinez_Synthetic-Data-Gen.pdf",
    "audit of pet-tau tracers for 24-month follow-up window": "2026-01-27_Daniel-Fischer_Weekly-Sync.pdf",
    "square root of dk scaling factor in attention": "2025-11-10_Chloe-Nguyen_Attention-Is-All-You-Need.pdf",
    "convergence of stochastic gradient descent in deep residuals": "2025-11-12_Chloe-Nguyen_Deep-Residual-Learning-for-Image-Recognition.pdf",
    "16x16 pixel image patch size for transformer recognition": "2025-11-15_Chloe-Nguyen_An-Image-is-Worth-16x16-Words-Transformers-for-Image-Recognition-at-Scale.pdf",
    "parametric generator and non-parametric retriever synergy": "2025-11-20_Chloe-Nguyen_Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.pdf",
    "bias correction using first and second moment estimates": "2025-11-22_Chloe-Nguyen_Adam-A-Method-for-Stochastic-Optimization.pdf",
    "co-learning and modality representation mismatch": "2025-11-05_Alice-Robertson_Multimodal-Machine-Learning-A-Survey-and-Taxonomy.pdf",
    "dynamic interventions in pathological protein networks": "2025-11-26_Alice-Robertson_A-Systemic-Pathological-Network-Model-and-Combinatorial-Intervention-Strategies-for-Alzheimers-Disease.pdf",
    "snapshot solver for graph models of neurodegeneration": "2025-11-29_Bob-Martinez_A-single-snapshot-inverse-solver-for-two-species-graph-model-of-tau-pathology-spreading-in-human-Alzheimer-disea.pdf",
    "longitudinal modeling of atrophy in alzheimers patient cohorts": "2025-12-02_Bob-Martinez_Data-driven-spatiotemporal-modeling-reveals-personalized-trajectories-of-cortical-atrophy-in-Alzheimers-disease.pdf",
    "stratification network performance across diverse alzheimers subtypes": "2025-12-04_Alice-Robertson_Pathology-Steered-Stratification-Network-for-Subtype-Identification-in-Alzheimers-Disease.pdf",
    "temporal reasoning benchmarks for traffic event qa": "2025-12-05_Bob-Martinez_SUTD-TrafficQA-A-Question-Answering-Benchmark-and-an-Efficient-Network-for-Video-Reasoning-over-Traffic-Events.pdf",
    "quantitative interpretation of brain region volumetric changes": "2025-12-07_Bob-Martinez_A-Quantitatively-Interpretable-Model-for-Alzheimers-Disease-Prediction-Using-Deep-Counterfactuals.pdf",
    "integrated analysis of pet scans and clinical cognitive scores": "2025-12-08_Chloe-Nguyen_Multimodal-Attention-based-Deep-Learning-for-Alzheimers-Disease-Diagnosis.pdf",
    "saliency map evaluation and disease relevant features": "2025-12-10_Alice-Robertson_A-Quantitative-Approach-for-Evaluating-Disease-Focus-and-Interpretability-of-Deep-Learning-Models-for-Alzheimers.pdf",
    "clinician centered explainable ai for critical care support": "2025-12-12_Chloe-Nguyen_Exploring-the-Requirements-of-Clinicians-for-Explainable-AI-Decision-Support-Systems-in-Intensive-Care.pdf",
    "3d medical analysis using transfer learning on large scale datasets": "2025-12-14_Bob-Martinez_Med3D-Transfer-Learning-for-3D-Medical-Image-Analysis.pdf",
    "adversarial training for medical image segmentation and denoising": "2025-12-16_Chloe-Nguyen_Generative-Adversarial-Network-in-Medical-Imaging-A-Review.pdf",
    "scientific team success through fresh perspectives": "2025-12-20_Daniel-Fischer_Freshness-Persistence-and-Success-of-Scientific-Teams.pdf",
    "economic analysis of scientific productivity in large collaborations": "2025-12-22_Daniel-Fischer_The-Link-Between-Large-Scientific-Collaboration-and-Productivity-Rethinking-How-to-Estimate-the-Monetary-Value-o.pdf",
    "researcher tool usage and perceptions survey results": "2025-12-24_Daniel-Fischer_LLMs-as-Research-Tools-A-Large-Scale-Survey-of-Researchers-Usage-and-Perceptions.pdf"
}

queries_traps = {
    # 1. THE ATTRIBUTION TRAP (Bob vs. Daniel)
    # Testing if the system can distinguish the source of a discovery from a summary.
    "primary discovery of tau-protein missingness in the proteomics dataset": "2026-01-14_Bob-Martinez_Proteomics-Integration.pdf",

    # 2. THE CHRONOLOGICAL/VERSION TRAP (Chloe Jan 16 vs. Bob Jan 22)
    # Chloe says alpha=8, Bob says alpha=50. A researcher wants the implementation log.
    "implementation parameters for bob martinez elastic transformations alpha and sigma": "2026-01-22_Bob-Martinez_Synthetic-Data-Gen.pdf",

    # 3. THE ADMINISTRATIVE PRIORITY TRAP (Compliance vs. Setup)
    # Testing if the system prioritizes the "Why/Rule" over the "How/Code".
    "formal institution policy on pseudonymization versus anonymization": "2026-01-05_Alice-Robertson_Compliance-Review.pdf",

    # 4. THE MODALITY OVERFITTING TRAP (Architecture vs. Results)
    # Chloe proposes fusion in one doc, but documents the branch failure in another.
    "empirical evidence of overfitting in the mri-only encoder branch": "2026-01-16_Chloe-Nguyen_Hyperparameter-Sweep.pdf",

    # 5. THE EXTERNAL VALIDATION TRAP (Protocol vs. Meeting)
    # Alice mandates the dataset; Daniel just prepares a template for it.
    "formal mandate for model evaluation on the oasis-3 dataset": "2026-01-12_Alice-Robertson_Evaluation-Standards.pdf",

    # 6. THE NUMERICAL INSTABILITY TRAP (Environment vs. Sweep)
    # Testing if "instability" leads to Hyperparameters (Common) or the specific NumPy fix.
    "resolution of floating-point overflows and nan values in mri preprocessing": "2026-01-18_Daniel-Fischer_Environment-Setup.pdf",

    # 7. THE "SALIENCY" ASSIGNMENT TRAP (Task List vs. Tech Proposal)
    # Testing if the system can find the assigned "Action Item" owner.
    "assignment of explainable ai xai saliency map generation": "2026-01-27_Daniel-Fischer_Weekly-Sync.pdf"
}


# ----------------------------------------
#          QUERY - 2 DOCUMENTS
# ----------------------------------------

queries_multi_documents = {
    "tau protein data missingness and audit results": [
        "2026-01-14_Bob-Martinez_Proteomics-Integration.pdf", 
        "2026-01-27_Daniel-Fischer_Weekly-Sync.pdf"
    ],
    "implementation and technical parameters of elastic deformation": [
        "2026-01-16_Chloe-Nguyen_Hyperparameter-Sweep.pdf", 
        "2026-01-22_Bob-Martinez_Synthetic-Data-Gen.pdf"
    ],
    "data processing agreement and prohibition of cloud services": [
        "2026-01-05_Alice-Robertson_Compliance-Review.pdf", 
        "2026-01-18_Daniel-Fischer_Environment-Setup.pdf"
    ],
    "mandatory metrics and the transition away from simple accuracy": [
        "2026-01-12_Alice-Robertson_Evaluation-Standards.pdf", 
        "2026-01-16_Chloe-Nguyen_Hyperparameter-Sweep.pdf"
    ],
    "transformer based bottleneck fusion architecture and cross attention layers": [
        "2026-01-08_Chloe-Nguyen_Multimodal-Fusion-Logic.pdf", 
        "2026-01-16_Chloe-Nguyen_Hyperparameter-Sweep.pdf", 
        "2026-01-27_Daniel-Fischer_Weekly-Sync.pdf"
    ],
    "integration and standardization of the oasis-3 dataset": [
        "2026-01-12_Alice-Robertson_Evaluation-Standards.pdf", 
        "2026-01-27_Daniel-Fischer_Weekly-Sync.pdf"
    ],
    "dockerized environment and training on the local h100 cluster": [
        "2026-01-18_Daniel-Fischer_Environment-Setup.pdf", 
        "2026-01-27_Daniel-Fischer_Weekly-Sync.pdf"
    ],
    "overfitting in mri encoder branch and its clinical regularization": [
        "2026-01-16_Chloe-Nguyen_Hyperparameter-Sweep.pdf", 
        "2026-01-27_Daniel-Fischer_Weekly-Sync.pdf"
    ],
    "augmentation strategies including smote and 3d mri transformations": [
        "2026-01-16_Chloe-Nguyen_Hyperparameter-Sweep.pdf", 
        "2026-01-22_Bob-Martinez_Synthetic-Data-Gen.pdf"
    ],
    "gdpr compliance and the distinction between pseudonymization and anonymization": [
        "2026-01-05_Alice-Robertson_Compliance-Review.pdf", 
        "2026-01-18_Daniel-Fischer_Environment-Setup.pdf"
    ]
}


queries_negative_easy = {
    "How to perform open-heart surgery on a pediatric patient": None,
    "Cooking recipes for a low-carb Mediterranean diet": None,
    "The impact of solar flares on satellite communications": None,
    "Historical analysis of the French Revolution": None,
    "Quantum computing algorithms for financial market prediction": None,
    "Best practices for organic gardening in urban environments": None,
    "How to repair a leaked pipe in a basement": None,
    "Top-rated tourist attractions in Tokyo for 2026": None,
    "The role of the central bank in controlling inflation": None,
    "Training a golden retriever puppy for agility competitions": None,
    "Aerodynamics of high-speed passenger trains": None,
    "Geological formations of the Grand Canyon": None,
    "Summary of the 2024 Olympic Games opening ceremony": None,
    "How to write a screenplay for a sci-fi movie": None,
    "Chemical composition of the Martian atmosphere": None,
    "Maintenance protocols for offshore wind turbines": None,
    "History of jazz music in New Orleans": None,
    "Psychological effects of social media on teenagers": None,
    "Standard operating procedures for commercial airlines": None,
    "Fashion trends for the 2026 spring season": None,
    "Design of earthquake-resistant skyscrapers": None,
    "How to brew craft beer at home": None,
    "Marine biology of the Great Barrier Reef": None,
    "Evolution of the internal combustion engine": None,
    "Ancient Egyptian mummification processes": None,
    "The physics of black hole singularities": None,
    "Rules of professional chess tournaments": None,
    "Architecture of Gothic cathedrals in Europe": None
}

queries_negative_intermediate = {
    "Using YOLOv8 for real-time detection of skin cancer": None,
    "Clinical efficacy of Donepezil in late-stage dementia": None,
    "Impact of Vitamin D on bone density in elderly women": None,
    "Diagnosis of Parkinson's disease using gait analysis": None,
    "Genetic markers for Type 2 Diabetes in Asian populations": None,
    "Robotic surgery protocols for neuro-oncology": None,
    "Treatment of chronic migraines with Botox injections": None,
    "Using XGBoost for predicting patient hospital readmission": None,
    "Managing electronic health records with the Epic platform": None,
    "Side effects of chemotherapy on heart health": None,
    "Protocols for lumbar punctures in pediatric patients": None,
    "Using GANs to generate synthetic chest X-rays for pneumonia": None,
    "Impact of exercise on resting heart rate in athletes": None,
    "Legal requirements for HIPAA compliance in California": None,
    "Diagnosis of pediatric ADHD using behavioral checklists": None,
    "Training Llama-3 on public medical journals for drug discovery": None,
    "The role of gut microbiome in inflammatory bowel disease": None,
    "Standard care for managing stage 4 lung cancer": None,
    "Evaluation of the 'Mini-Mental State Exam' for healthy students": None,
    "Using Apache Spark for distributed genomic sequencing": None,
    "Effectiveness of cognitive behavioral therapy for anxiety": None,
    "Analyzing the impact of sleep apnea on cardiovascular health": None,
    "Using Graph Neural Networks for modeling chemical toxicity": None,
    "Integrating the 'MIMIC-III' dataset for patient mortality prediction": None,
    "Financial audit of a 2025 cancer research grant": None,
    "Ethical guidelines for neural implants in neuro-prosthetics": None,
    "Comparison between ResNet-101 and DenseNet for malaria detection": None,
    "Clinical trial results for a new leukemia treatment": None
}

queries_negative_difficult = {
    "Clinical efficacy of Aducanumab in phase 3 trials": None,
    "Using Kubernetes for GPU orchestration in medical clusters": None,
    "Impact of Vitamin E on cognitive decline in late-stage dementia": None,
    "Training Llama 3 on private patient medical records": None,
    "Deploying models to AWS SageMaker via Terraform scripts": None,
    "Real-time patient monitoring using wearable IoT devices for Parkinson's": None,
    "HIPAA-compliant data storage in California state clouds": None,
    "Genetic markers for Type 2 Diabetes in European cohorts": None,
    "Comparing YOLOv10 performance on surgical video feeds": None,
    "Using Gated Recurrent Units (GRU) for temporal cognitive modeling": None,
    "Financial audit of the 2024 neuro-oncology grant": None,
    "Impact of Mediterranean diet on hippocampal volume": None,
    "Setting up a Slurm cluster for distributed training on A100 GPUs": None,
    "Using GANs to generate synthetic chest X-rays for pneumonia": None,
    "Analysis of the impact of sleep apnea on Amyloid-beta clearance": None,
    "Comparison between ResNet-101 and DenseNet-201 for skin lesion classification": None,
    "Managing clinical trials through the 'Medidata Rave' platform": None,
    "Protocols for lumbar puncture in pediatric neurology": None,
    "Using Reinforcement Learning from Human Feedback (RLHF) for medical chatbots": None,
    "The role of Apolipoprotein E (APOE) ε2 allele in longevity": None,
    "Building a data lake on Google Cloud Storage (GCS) for genomics": None,
    "Evaluation of the 'Mini-Mental State Exam' (MMSE) scores in healthy teenagers": None,
    "Using Graph Convolutional Networks (GCN) for modeling chemical toxicity": None,
    "Integrating the 'MIMIC-IV' dataset into the AD-Fusion pipeline": None,
    "Ethical guidelines for using brain-computer interfaces in sports": None,
    "Using Apache Spark for distributed preprocessing of genomic VCF files": None,
    "The effect of caffeine consumption on Tau-protein phosphorylation": None,
    "Training Vision Transformers (ViT) on the ImageNet-21k dataset": None
}