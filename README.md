# Chatbot Fine-Tuned on Custom Context (French Language)

## Project Overview

This project aims to develop a smart chatbot `fine-tuned` on a custom context based on the French language, specifically for the `Faculty of Sciences and Techniques of Tangier (FSTT)`. The chatbot leverages advanced NLP techniques such as Retrieval Augmented Generation (RAG), LangChain, and vector databases (Chroma) to provide accurate and contextually relevant responses.

### Structure of the project 


```markdown
chatbot/
├── .idea/
├── chatbot-app/
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── App.test.js
│   │   ├── feather-icons.css
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── logo.svg
│   │   ├── reportWebVitals.js
│   │   └── setupTests.js
│   ├── .gitignore
│   ├── README.md
│   ├── package-lock.json
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile  # Dockerfile for frontend
├── flask-api/
│   ├── chroma/
│   │   └── chroma.sqlite3
│   ├── rag_project/
│   │   ├── .idea/
│   │   ├── __pycache__/
│   │   ├── chroma/
│   │   ├── rag_project.egg-info/
│   │   ├── data_processing.py
│   │   ├── embeddings.py
│   │   ├── install_dependencies.py
│   │   ├── main.py
│   │   ├── query_model.py
│   │   ├── requirements.txt
│   │   ├── setup.py
│   │   └── app.py
│   ├── .gitattributes
│   ├── requirements.txt
│   └── Dockerfile  # Dockerfile for backend
└── docker-compose.yml
```

### Introduction and Motivation:

The goal is to create a sophisticated chatbot capable of understanding and responding in French, tailored to the specific context of FSTT. This project uses cutting-edge NLP techniques such as Retrieval Augmented Generation (RAG), LangChain, and vector databases to enhance the chatbot's performance and relevance.

### Motivation :


- **RAG and LangChain:** These technologies allow the chatbot to generate more accurate and contextually appropriate responses by leveraging a combination of retrieval-based and generative methods.
- **Vector Databases:** `Chroma` helps in efficiently storing and querying high-dimensional data, which is essential for handling the embeddings used in NLP models.

### Literature Review:

A brief overview of existing chatbot technologies, focusing on advancements in Arabic and French language processing, was conducted. This review helped identify the unique challenges and opportunities in developing a chatbot for FSTT.

#### Data Collection

Data about FSTT, including courses, activities, and other relevant information, was collected using web scraping technique especially `scrapy framework` , this is the link of the repository of the scraping process : [https://github.com/HAFDAOUIH/Crawl_FSTT.git] that provide an incredible integration with database easiest scraping with css selector 

### Fine-Tuning Process:
#### Dataset Preparation:

- The data was processed and formatted into `instructions` and `responses`.
- A `custom prompt` format was created to enhance the training process.

#### Model Selection:

`Mistral-7B-Instruct-v0.3` was chosen for its advanced capabilities in handling French language tasks and `arabic` also.

#### Training:

- The model was fine-tuned using `LoRA` (Low-Rank Adaptation) to optimize for performance and efficiency.
- he training was conducted on `Kaggle` to leverage its `computational resources`.

#### Implementation:

- The chatbot backend was implemented using `Flask`, and the frontend using `React`.
- `Docker` was used to containerize the applications for easy deployment.

### Tools and Technologies

- `LLMs (Mistral, Ollama(Mistral))`
- `LangChain`
- `Vector Databases (Chroma)`
- `LLMOps, Fine Tuning, LoRA/QLoRA`
- `Quantization (float32 – int8)`
- `PEFT (Parameter Efficient Fine-Tuning)`
- `ReactJS, Flask, Docker`
- `Arabic NLP, Data Augmentation, Scrapy Framework`
- `Prompt Engineering`


### Backend Development
#### Choice of Framework

`Flask` was chosen for its simplicity, flexibility, and scalability, making it suitable for building `RESTful APIs`.


### DevOps Integration

Continuous Integration and `Deployment (CI/CD)` were integrated using `Docker`, ensuring smooth and efficient development workflows.

### Single Page Application (SPA)
#### Architecture

The frontend was developed as a `Single Page Application` using `React`, offering a seamless and interactive user experience.
Benefits and Challenges

    Benefits: Enhanced user experience, faster interactions, and easier state management.
    Challenges: Handling initial load times and ensuring SEO optimization.

### Language Model Training
#### Process

The language models were fine-tuned to account for the linguistic nuances and cultural contexts of French, particularly in the context of FSTT.
#### Challenges

Limited availability of training data.
Potential challenges in capturing cultural and linguistic nuances accurately.

### User Interface (UI) Design
#### Accessibility and Cultural Considerations

The UI was designed to be accessible and user-friendly, aligning with the cultural preferences of the target audience.

## Docker Setup

### Building the Docker Images

Navigate to the project root directory and execute the following commands to build the Docker images:

```bash
docker-compose build
```

### Running the Containers

#### Start the containers using:
```bash
docker-compose up
```

####  Run the containers
#### Run container of front-end:
    docker run -d -p 80:80 nlp_chatbot-frontend
#### Run container of back-end:
    docker run -d -p 80:80 chatbot-frontend
