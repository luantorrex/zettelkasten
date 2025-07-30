# Zettelkasten

![Zettelkasten Diagram](https://raw.githubusercontent.com/luantorrex/zettelkasten/refs/heads/main/zettelkasten.png)

This repository contains the skeleton of an MVC-based microservice that will perform CRUD operations on a MongoDB database. The service is intended to manage Zettelkasten notes in a simple and extensible manner.

## Overview

- **Architecture**: Model–View–Controller (MVC)
- **Database**: MongoDB
- **Features**: Create, read, update, and delete notes
- **CORS**: Enabled for all origins by default

## Status

Implementation is not yet complete. Future commits will include the API source code and setup instructions.

## Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
