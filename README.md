---
colorTo: coral
colorFrom: green
emoji: ✨
license: bsd-2-clause
title: Data Mapper
sdk: gradio
---

# LLM Data Mapper

## Overview
This app uses an LLM to generate a mapping between a source and target (template) schema, executing python code to complete the transformation. Of course, there are more efficient ways to create such a pipeline, but this is mostly an exercise in how an LLM would perform and how it might contribute to a human-in-the-loop ETL user experience.

A guiding principle is that the LLM should do the mapping, not the transforming. For large datasets, we will quickly bump up against the constraint of time, token cost, and context window length.

## Tech
- Langchain 
- OpenAI (GPT-4 ChatCompletion)
- Gradio
- Pandas
- Pydantic
- Weights and Biases

## Critiques
- The UI is basic and clunky. I can do a better job conditionall rendering components, providing feedback to the user, including undo buttons and other interactivity, etc.
- It is slow. I can do more to make the prompting more efficient and explore using lighter-weight models.
- There is very little error handling, though we get some for free from gradio and langchain.
- The prompts can be tuned better with in-context learning examples that are specific to the incoming data. 
- The Spec Writer -> Python Engineer might be excessive. I enjoyed exploring this personification of the workflow, but ultimately I'm not convinced it's contributing directly to an improvement in output.

## Approach
Given that this is an ETL pipeline, I decided to make everything as structured as possible. For example, I'm using the PydanticOutputParser to kick-off the mapping workflow, as I've found that helps make the LLM output more precise. In addition, the LLM temperature is at 0. And I decided to personify the prompts, so that each chain was one piece of a team working on a data transformation task. I'm not convinced that chaining

## Brainstorming
I left the brainstorming notebooks in the repo, showing the different approaches I took at the onset. 

### RCI Chains
I've had great success with [Recursive Criticism and Improvement](https://arxiv.org/abs/2303.17491) chains in the past and explored using them here (brainstorm3.ipynb), but ultimately thought it was excessive, as the current `Data Scientist` chain was able to generate the structured mapping file fine without an additional pass.

### SQL Agent
I think an agent-based system that is reading from and writing to a relational database would probably perform better, but ultimately I found the human-in-the-loop UX to be a bit difficult to implement in a short amount of time. Also, I thought the data model might be wonky, given that we'd reading ffrom and writing to temp tables, as we handled the transforms.

### Pandas Chains
Langchain has a Pandas Agent / Chain in the core library, but unfortunately I haven't had much luck with it in the past. This was no different. It's particularly error-prone when working with the OpenAI Functions API, as it usually generates output that cannot be serialized. After spending a good amount of time handling errors, I decided to scrap it and move on to 
