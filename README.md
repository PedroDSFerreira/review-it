# Review-it

Review-it is a microservice platform that enables users to create, manage, and view reviews for specific entities, such as products or services, within a distributed system architecture.

## Features

* **🧱 Entities**

  * Services can define entities that need reviews (e.g., products, listings).
  * An entity represents any reviewable item on the platform.

* **📝 Reviews**

  * Users can write, edit, and manage reviews for each entity.

* **🔐 Authentication**

  * JWT via Auth0 for user login.
  * API tokens for service-to-service communication.

* **🔍 Pagination & Filtering**

  * List endpoints support pagination and filtering.
  * Option to retrieve all results at once.

* **📘 API Docs**

  * OpenAPI/Swagger docs are auto-generated and available via a web UI.

* **💻 Embeddable Review UI**

  * Drop-in HTML interface to show and manage reviews.
  * Users can create, edit, and delete reviews directly from it.

* **🧪 Testing & Quality**

  * Unit tests for models and authentication.
  * GitHub Actions for automated testing and security checks.

* **🚀 Deployment**

  * Easy setup with Docker and Docker Compose.
  * Health checks and persistent storage included.
  * Kubernetes support available.


## Requirements

- **Docker**
- **Make**

## Setup

1. **Clone the Repository**

   Clone the project repository and navigate into the project directory:

   ```bash
   git clone <repository-url>
   cd review-it
   ```

2. **Prepare Environment Variables**

   Copy the sample environment file to create your own `.env` file:

   ```bash
   make prepare-env
   ```

   Edit the `.env` file as needed to configure your credentials and settings.

3. **Build the Docker Images**

   Build the Docker images for both the application and the database:

   ```bash
   make build
   ```

4. **Start the Services**

   Use Docker Compose to start the services. You have two options:

   ```bash
     make upd
   ```

5. **Run Database Migrations**

   Once the services are running, create and apply database migrations:

   ```bash
   make makemigrations
   make migrate
   ```

- **Generate API Documentation (Optional)**

  The project includes a Swagger (OpenAPI) specification for the API. Generate the API documentation with:

  ```bash
  make generate-docs
  ```

  This will produce a `swagger.yaml` file detailing all available endpoints, models, and authentication methods.

- **Accessing the Containers:**

  - **Application Container:**
    ```bash
    make exec
    ```
  - **Database Container:**
    ```bash
    make db-exec
    ```

## API Overview

- **Entities:**

  - `GET /api/v1/entities/` – List entities (supports pagination).
  - `POST /api/v1/entities/` – Create a new entity.
  - `GET /api/v1/entities/{id}/` – Retrieve a specific entity.
  - `PUT /api/v1/entities/{id}/` – Update an existing entity.
  - `DELETE /api/v1/entities/{id}/` – Delete an entity.

- **Reviews:**
  - `GET /api/v1/entities/{entity_pk}/reviews/` – List reviews for an entity (supports pagination).
  - `POST /api/v1/entities/{entity_pk}/reviews/` – Create a review for an entity.
  - `GET /api/v1/entities/{entity_pk}/reviews/{id}/` – Retrieve a specific review.
  - `PUT /api/v1/entities/{entity_pk}/reviews/{id}/` – Update a review.
  - `DELETE /api/v1/entities/{entity_pk}/reviews/{id}/` – Delete a review.

Authentication is handled via two methods:

- **Token-based Authentication:** Use a header with the format `Token <your_api_token>`, to manage entities.
- **JWT Authentication (Auth0):** Use a header with the format `Bearer <your_jwt_token>`, to manage reviews.

For further details, refer to the generated `swagger.yaml` file.

## Embeddable Review UI

Review-it provides an embeddable HTML interface that allows you to display and manage reviews for any entity directly within your own website or application. This UI is styled with Bootstrap and supports:

- Viewing paginated reviews for a specific entity.
- Creating and managing your own reviews (if authenticated with a JWT).
- Interactive star ratings and modals for review actions.

To use the embed, simply include the appropriate URL (e.g., `/embed/entities/<entity_id>/reviews`) in an iframe or as a standalone page.  
You can pass the user JWT token as a query parameter (`?token=...`) to enable actions for users.

This makes it easy to integrate reviews into any web platform with minimal setup.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
