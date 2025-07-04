# Detailed Report Generator Using Orchestrator-Worker

### How To Execute 

1) pip install -r requirements.txt
2) python "file_name".py
3) Make sure to add .env file with your own groq API key

### Explanation

This code **automatically writes a report** using AI.

You just give it a **topic**, like “Agentic AI RAGs” — and it will:

1. **Break the topic** into smaller parts.
2. **Write content** for each part using AI.
3. **Join everything** together into one final report.

### What are the parts?

#### 1. **Planner**

* Think of this like a teacher making a lesson plan.
* It breaks the big topic into 3–5 smaller sections.

  > Example: “Introduction”, “How it works”, “Benefits”

#### 2. **Workers**

* Each worker takes one section and **writes the content** for it.
* They all work **at the same time** (in parallel).

  > This saves time and makes it faster.

#### 3. **Orchestrator**

* This is the **manager**.
* It tells the planner what to do, assigns sections to the workers, and waits until they finish.

#### 4. **Synthesizer**

* It **joins all the parts** written by the workers.
* Then gives you one clean, full report in markdown format.

### Flow of Work (Simple Steps)

1. You give a topic (like: “Create a report on Agentic AI RAGs”).
2. The **planner** breaks it into smaller topics.
3. The **workers** write each section.
4. The **synthesizer** puts everything together.
5. You get a nice, full report.

### What do you get at the end?

A full report like this (in markdown format):

```markdown
## Introduction to Agentic AI

(content written by AI)

------

## What is RAG (Retrieval-Augmented Generation)?

(content written by AI)

------

## Future Scope and Applications

(content written by AI)
```

---

### 🎯 Why is this useful?

* Saves a lot of time
* Everything is automated
* Works for any topic you give