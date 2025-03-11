# Review-it

Review-it is a review platform microservice that allows users to create reviews for specific

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

- **Token-based Authentication:** Use a header with the format `Token <your_api_token>`.
- **JWT Authentication (Auth0):** Use a header with the format `Bearer <your_jwt_token>`.

For further details, refer to the generated `swagger.yaml` file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
