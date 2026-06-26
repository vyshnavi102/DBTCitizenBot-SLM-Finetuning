# Project Overview

## Project Title

**DBT Citizen Bot – Domain-Specific Small Language Model (SLM) Fine-Tuning**

---

# 1. Project Overview

The DBT Citizen Bot is an AI-powered assistant designed to help citizens discover and understand various Government schemes by answering queries in natural language. The existing system uses a Retrieval-Augmented Generation (RAG) architecture that retrieves relevant scheme information from a curated knowledge base and generates responses for users.

To understand user queries, the current pipeline relies on multiple prompt-based language model calls combined with deterministic business rules for tasks such as Intent Classification, Scope Detection, Filter Extraction, and Response Generation.

As the number of government schemes, departments, filters, and multilingual queries continues to grow, maintaining numerous prompts and business rules becomes increasingly complex. This project aims to simplify and improve the query understanding pipeline by developing a domain-specific Small Language Model (SLM) through parameter-efficient fine-tuning.

The fine-tuned model will specialize in understanding DBT-related user queries while continuing to leverage the existing RAG pipeline for retrieving dynamic scheme information.

---

# 2. Project Objectives

The primary objective of this project is to build a domain-specific language model capable of accurately understanding user queries related to DBT schemes.

The model will be trained to perform the following tasks:

* Intent Classification
* Scope Detection
* Filter Extraction
* Marathi and English Query Understanding
* Natural Response Generation using retrieved RAG context

The project will **not** train the model to memorize government scheme information. Instead, it will improve how the system interprets user queries before passing them to the existing retrieval pipeline.

---

# 3. Existing System

The current Citizen Bot follows the architecture below:

User Query

↓

Scope Detection

↓

Intent Classification

↓

Filter Extraction

↓

Profile Manager

↓

Hard Filter

↓

Adaptive RAG Retrieval

↓

Answer Generation

Most of the query-understanding stages are currently implemented using prompt engineering and multiple language model calls.

---

# 4. Proposed Solution

The proposed solution introduces a fine-tuned Qwen3-14B model that replaces multiple prompt-based query-understanding components with a single task-specific model.

The proposed workflow is:

User Query

↓

Fine-Tuned Qwen3-14B Task Model

↓

Intent + Scope + Filters

↓

Profile Manager

↓

Hard Filter

↓

Adaptive RAG Retrieval

↓

Natural Language Response Generation

↓

User

The retrieved scheme information will continue to come from the existing RAG pipeline, ensuring that responses always use the latest scheme data.

---

# 5. Scope of the Project

The project focuses on improving the intelligence layer responsible for understanding user queries.

### In Scope

* Fine-tuning a domain-specific Small Language Model
* Dataset preparation
* Marathi and English query understanding
* Intent Classification
* Scope Detection
* Filter Extraction
* Response Formatting
* Integration with the existing Citizen Bot pipeline
* Model evaluation and benchmarking

### Out of Scope

The model will not be trained to memorize:

* Scheme details
* Eligibility criteria
* Benefits
* Required documents
* Application procedures
* Dynamic scheme information

These will continue to be retrieved using the existing Retrieval-Augmented Generation (RAG) system.

---

# 6. Proposed Technology

The project will use:

* Qwen3-14B as the base language model
* QLoRA for parameter-efficient fine-tuning
* Hugging Face Transformers
* PEFT
* BitsAndBytes
* TRL
* PyTorch
* vLLM for model serving
* LangGraph for workflow orchestration
* Qdrant for vector retrieval
* Existing RAG pipeline for dynamic knowledge retrieval

---

# 7. Expected Outcomes

Upon completion, the system is expected to provide:

* Improved query understanding
* Better multilingual (Marathi and English) support
* Higher filter extraction accuracy
* Reduced prompt engineering effort
* Fewer model calls
* Lower response latency
* Better maintainability
* Seamless integration with the existing RAG architecture

---

# 8. Repository Structure

This repository contains all research, implementation, datasets, experiments, and documentation related to the development of the domain-specific DBT task model.

Major components include:

* Project Documentation
* Research and R&D
* Dataset Preparation
* Fine-Tuning Implementation
* Model Evaluation
* Integration
* Benchmark Reports

---

# 9. Project Deliverables

The project is expected to deliver:

* Domain-specific training datasets
* Fine-tuned Qwen3-14B adapter
* Model evaluation reports
* Integration with the Citizen Bot
* Updated architecture documentation
* Performance benchmarking reports
* Complete implementation documentation

---

# 10. Conclusion

This project aims to enhance the DBT Citizen Bot by developing a domain-specific Small Language Model that specializes in understanding citizen queries while preserving the existing Retrieval-Augmented Generation (RAG) architecture for dynamic scheme retrieval.

By combining parameter-efficient fine-tuning with the current retrieval pipeline, the solution seeks to improve accuracy, multilingual support, maintainability, and scalability without requiring the model to memorize frequently changing government scheme information.
